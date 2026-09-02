from services.entity_extractor import (
    extract_company_name,
)


QUESTIONS = [
    "What is Price LLC's refund window?",
    "How much revenue did Austin, Day and Johnson generate?",
    "What is Wilson, Pena and Rich's contract value?",
    "Which customer generated the most revenue?",
    "How many customers do we have?",
    "Tell me about the refund policy.",
]


def main():

    print("=" * 70)
    print("ENTITY EXTRACTION TEST")
    print("=" * 70)

    for question in QUESTIONS:

        company = extract_company_name(
            question
        )

        print("\nQuestion:")
        print(question)

        print(
            f"Company: {company}"
        )


if __name__ == "__main__":
    main()