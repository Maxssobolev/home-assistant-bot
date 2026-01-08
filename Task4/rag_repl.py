from rag_core import load_vectorstore, answer_query, get_security_flags

def print_security_flags(flags: dict):
    print("Security configuration:")
    print(f"- Pre-prompt protection: {'ENABLED' if flags['ENABLE_PRE_PROMPT'] else 'DISABLED'}")
    print(f"- Post-filter (malicious chunks): {'ENABLED' if flags['ENABLE_POST_FILTER'] else 'DISABLED'}")
    print(f"- Context sanitization: {'ENABLED' if flags['ENABLE_SANITIZE'] else 'DISABLED'}")
    print("")

def main():
    db, _ = load_vectorstore()
    
    flags = get_security_flags()
    print("RAG Bot started. Для выхода: Ctrl+C")
    print_security_flags(flags)
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
