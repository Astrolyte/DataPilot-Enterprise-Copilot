from services.hybrid import ask_hybrid


def main():

    question = (
        "What is Price LLC's refund window and "
        "how much revenue has Price LLC generated "
        "from completed orders?"
    )

    print("=" * 70)
    print("HYBRID QUERY")
    print("=" * 70)

    print("\nQuestion:")
    print(question)

    result = ask_hybrid(
        company_name="Price LLC",
        question=question,
    )

    print("\n" + "-" * 70)
    print("ANSWER")
    print("-" * 70)

    print(result["answer"])

    print("\n" + "-" * 70)
    print("SOURCES")
    print("-" * 70)

    print(
        f"Customer: "
        f"{result['customer']['company_name']}"
    )

    print(
        f"Document: "
        f"{result['document_id']}"
    )

    print(
        f"Completed revenue: "
        f"{result['revenue']['completed_revenue']}"
    )


if __name__ == "__main__":
    main()