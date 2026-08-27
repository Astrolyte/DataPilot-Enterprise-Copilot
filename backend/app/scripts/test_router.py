from services.router import route_question


QUESTIONS = [
    "How many customers do we have?",
    "Which customer generated the most completed revenue?",
    "What is the refund policy?",
    "How much PTO does a full-time employee receive?",
    "What is Price LLC's refund window?",
    "What is Price LLC's refund window and how much revenue has Price LLC generated from completed orders?",
]


def main():

    print("=" * 70)
    print("DataPilot Query Router")
    print("=" * 70)

    for question in QUESTIONS:

        route = route_question(question)

        print("\nQuestion:")
        print(question)

        print(f"Route: {route}")


if __name__ == "__main__":
    main()