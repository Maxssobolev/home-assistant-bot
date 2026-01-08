import os
import time
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


KNOWLEDGE_DIR = "Task2/knowledge_base"
INDEX_DIR = "faiss_index"

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

SPLITTER = RecursiveCharacterTextSplitter(
    chunk_size=1500,
    chunk_overlap=200,
    length_function=len,
    separators=["\n\n", "\n", ". ", " ", ""],
)


@dataclass
class ChunkDoc:
    text: str
    metadata: Dict[str, Any]


def read_documents(dir_path: str) -> List[Tuple[str, str]]:
    files = sorted(
        f for f in os.listdir(dir_path)
        if f.endswith(".md") or f.endswith(".txt")
    )
    if not files:
        raise SystemExit(f"Папка {dir_path} пуста")

    docs: List[Tuple[str, str]] = []
    for fn in files:
        path = os.path.join(dir_path, fn)
        with open(path, "r", encoding="utf-8") as f:
            docs.append((fn, f.read()))
    return docs


def make_chunks(docs: List[Tuple[str, str]]) -> List[ChunkDoc]:
    out: List[ChunkDoc] = []
    for file_name, text in docs:
        # Вытаскиваем заголовок из первой строки md, если есть
        title = ""
        first_line = text.splitlines()[0].strip() if text.strip() else ""
        if first_line.startswith("#"):
            title = first_line.lstrip("#").strip()

        chunks = SPLITTER.split_text(text)

        for i, chunk in enumerate(chunks):
            out.append(
                ChunkDoc(
                    text=chunk,
                    metadata={
                        "source": file_name,
                        "title": title or file_name,
                        "chunk_id": i,
                        "chunk_total": len(chunks),
                    },
                )
            )
    return out


def main():
    start = time.time()

    os.makedirs(INDEX_DIR, exist_ok=True)

    docs = read_documents(KNOWLEDGE_DIR)
    chunk_docs = make_chunks(docs)

    texts = [c.text for c in chunk_docs]
    metadatas = [c.metadata for c in chunk_docs]

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

    # Строим индекс
    db = FAISS.from_texts(texts=texts, embedding=embeddings, metadatas=metadatas)

    # Сохраняем на диск
    db.save_local(INDEX_DIR)

    elapsed = time.time() - start

    print("Индекс построен и сохранен.")
    print(f"Папка индекса: {INDEX_DIR}/")
    print(f"Документов: {len(docs)}")
    print(f"Чанков: {len(chunk_docs)}")
    print(f"Модель: {EMBEDDING_MODEL_NAME} (dim=384)")
    print(f"Время генерации: {elapsed:.2f} сек")


if __name__ == "__main__":
    main()
