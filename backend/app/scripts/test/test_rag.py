from services.rag import ask


def main():

    print("\n" + "=" * 70)
    print("DataPilot RAG")
    print("Type 'exit' to quit")
    print("=" * 70)

    while True:

        question = input("\nAsk DataPilot: ").strip()

        if question.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        if not question:
            continue

        try:

            result = ask(question=question,user_role="admin",top_k=3,)

            print("\n" + "=" * 70)
            print("ANSWER")
            print("=" * 70)

            print(result["answer"])

            print("\n" + "=" * 70)
            print("SOURCES")
            print("=" * 70)

            for source in result["sources"]:

                print(f"\nDocument: "f"{source['document_id']}")

                print(f"File: "f"{source['source_file']}")

                print(f"Score: "f"{source['score']:.4f}")

        except Exception as e:

            print("\nError:")
            print(e)


if __name__ == "__main__":
    main()