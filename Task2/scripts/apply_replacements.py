import json
import os
import re
from typing import Dict, List, Tuple


def load_terms_map(path: str) -> Dict[str, str]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_patterns(terms_map: Dict[str, str]) -> List[Tuple[re.Pattern, str]]:
    items = sorted(terms_map.items(), key=lambda kv: len(kv[0]), reverse=True)

    patterns: List[Tuple[re.Pattern, str]] = []
    for src, dst in items:
        pat = re.compile(rf"(?<!\w){re.escape(src)}(?!\w)", flags=re.IGNORECASE)
        patterns.append((pat, dst))
    return patterns


def preserve_case(src_match: str, replacement: str) -> str:
    if src_match.isupper():
        return replacement.upper()
    if src_match[:1].isupper() and src_match[1:].islower():
        return replacement[:1].upper() + replacement[1:]
    return replacement


def apply_all(text: str, patterns: List[Tuple[re.Pattern, str]]) -> str:
    out = text
    for pat, repl in patterns:
        def _sub(m: re.Match) -> str:
            return preserve_case(m.group(0), repl)
        out = pat.sub(_sub, out)
    return out


def main():
    terms_map = load_terms_map("terms_map.json")
    patterns = build_patterns(terms_map)

    os.makedirs("knowledge_base", exist_ok=True)

    in_dir = "raw_pages"
    files = [f for f in os.listdir(in_dir) if f.endswith(".md") or f.endswith(".txt")]

    if not files:
        raise SystemExit("Нет файлов в raw_pages/. Сначала запустите fetch_and_clean.py")

    for fn in files:
        src_path = os.path.join(in_dir, fn)
        dst_path = os.path.join("knowledge_base", fn)

        with open(src_path, "r", encoding="utf-8") as f:
            txt = f.read()

        replaced = apply_all(txt, patterns)

        with open(dst_path, "w", encoding="utf-8") as f:
            f.write(replaced)

    print(f"Готово: knowledge_base/ ({len(files)} файлов).")


if __name__ == "__main__":
    main()
