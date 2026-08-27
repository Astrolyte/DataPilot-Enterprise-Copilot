from services.sql import ask_sql


def main():

    print("=" * 70)
    print("DataPilot SQL")
    print("Type 'exit' to quit")
    print("=" * 70)

    while True:

        question = input(
            "\nAsk a data question: "
        ).strip()

        if question.lower() in {
            "exit",
            "quit",
        }:
            break

        if not question:
            continue

        try:

            result = ask_sql(question)

            print("\n" + "-" * 70)
            print("Generated SQL")
            print("-" * 70)

            print(result["sql"])

            print("\n" + "-" * 70)
            print("Results")
            print("-" * 70)

            for row in result["rows"]:
                print(row)

        except Exception as e:

            print("\nERROR:")
            print(e)


if __name__ == "__main__":
    main()