import os
import re
import time
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; RAG-KB-Builder/1.0; +local)"
}


def slug_from_url(url: str) -> str:
    path = urlparse(url).path.strip("/")
    slug = path.split("/")[-1] or "page"
    slug = re.sub(r"[^a-zA-Z0-9_\-]+", "_", slug)
    return slug[:120]


def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_main_text(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")

    # Убираем явный мусор
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    # На fandom основной контент часто лежит в .mw-parser-output
    main = soup.select_one(".mw-parser-output")
    if not main:
        main = soup.body or soup

    # Убираем таблицы навигации, инфобоксы и прочие блоки, если попались
    for bad in main.select(
        ".portable-infobox, .toc, .navbox, .infobox, .reference, sup, .mw-editsection"
    ):
        bad.decompose()

    text = main.get_text(separator="\n")

    # Удаляем типичные "хвосты" и повторяющиеся служебные строки
    lines = []
    for line in text.split("\n"):
        s = line.strip()
        if not s:
            lines.append("")
            continue
        if s.lower() in {"contents", "navigation", "edit", "view source"}:
            continue
        lines.append(s)

    return normalize_text("\n".join(lines))


def read_pages_list(path: str) -> list[str]:
    with open(path, "r", encoding="utf-8") as f:
        urls = [ln.strip() for ln in f if ln.strip() and not ln.strip().startswith("#")]
    return urls


def main():
    os.makedirs("raw_pages", exist_ok=True)

    urls = read_pages_list(os.path.join("scripts", "pages.txt"))

    for i, url in enumerate(urls, start=1):
        slug = slug_from_url(url)
        out_path = os.path.join("raw_pages", f"{slug}.md")

        print(f"[{i}/{len(urls)}] GET {url}")
        r = requests.get(url, headers=HEADERS, timeout=30)
        r.raise_for_status()

        text = extract_main_text(r.text)

        # Минимальная структура в md: заголовок + тело
        title = slug.replace("_", " ")
        md = f"# {title}\n\n{text}\n"

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(md)

        time.sleep(1.0)

    print("Готово: raw_pages/ заполнена.")


if __name__ == "__main__":
    main()
