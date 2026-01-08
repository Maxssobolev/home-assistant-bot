from rag_core import load_vectorstore, answer_query


def main():
    db, _ = load_vectorstore()

    print("RAG REPL. Введите вопрос. Для выхода: Ctrl+C")
    print("Примеры запросов, которые можно попробовать:")
    print("- Что такое Synth Flux?")
    print("- Кто такие Aster Monks?")
    print("- Что такое Void Spindle?")
    print("- Какие цели у Helion Dominion?")
    print("")
    while True:
        q = input("\n> ").strip()
        if not q:
            print("Введите непустой запрос.")
            continue

        res = answer_query(db, q)

        print("\n--- Ответ ---\n")
        print(res["answer"])
        print("\n--- Использовано чанков:", res["used_chunks"], "---")
        if res["sources"]:
            print(res["sources"])
        else:
            print("Источники: нет")


if __name__ == "__main__":
    main()
