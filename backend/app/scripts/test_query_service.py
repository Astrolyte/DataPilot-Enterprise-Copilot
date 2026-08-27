from services.query_service import process_question


def main():

    tests = [
        (
            "How many customers do we have?",
            "admin",
        ),
        (
            "What is the refund policy?",
            "finance",
        ),
        (
            "What is Price LLC's refund window and "
            "how much revenue has Price LLC generated "
            "from completed orders?",
            "finance",
        ),
    ]

    for question, role in tests:

        print("\n" + "=" * 70)
        print(f"Question: {question}")
        print("=" * 70)

        try:

            result = process_question(
                question=question,
                user_role=role,
            )

            print(
                f"Route: {result['route']}"
            )

            print(
                f"Result:\n{result['result']}"
            )

        except Exception as e:

            print(f"ERROR: {e}")


if __name__ == "__main__":
    main()