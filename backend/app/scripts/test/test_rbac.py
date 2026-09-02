from services.retriever import retrieve


def test(role):

    print("\n" + "=" * 60)

    print(f"USER ROLE: {role}")

    print("=" * 60)

    results = retrieve(
        query="What is the refund policy?",
        user_role=role,
        top_k=5,
    )

    for result in results:

        print(f"\nScore: {result['score']:.4f}")

        print(f"Document: "f"{result['document_id']}")

        print(f"Source: "f"{result['source_file']}")

        print(f"Allowed roles: "f"{result['allowed_roles']}")


def main():

    test("finance")

    test("sales")

    test("hr")

    test("admin")


if __name__ == "__main__":
    main()