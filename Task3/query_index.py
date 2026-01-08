from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


INDEX_DIR = "faiss_index"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def main():
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    db = FAISS.load_local(INDEX_DIR, embeddings, allow_dangerous_deserialization=True)

    query = "Кто такой FU-51-H1?"
    results = db.similarity_search(query, k=4)

    print(f"Запрос: {query}\n")
    for i, doc in enumerate(results, start=1):
        md = doc.metadata
        print(f"--- RESULT {i} ---")
        print(f"source: {md.get('source')}")
        print(f"title: {md.get('title')}")
        print(f"chunk: {md.get('chunk_id')}/{md.get('chunk_total')}")
        print("")
        print(doc.page_content[:800].strip())
        print("")


if __name__ == "__main__":
    main()
