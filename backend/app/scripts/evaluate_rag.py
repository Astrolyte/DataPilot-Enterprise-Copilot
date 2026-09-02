import json
from pathlib import Path

from app.services.rag import ask


EVAL_FILE = Path(
    "app/data/evaluation/rag_questions.json"
)


def load_questions():

    with EVAL_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:

        return json.load(file)


def evaluate_sources(
    results,
    expected_documents,
):

    retrieved_documents = {
        result["document_id"]
        for result in results
    }

    expected_documents = set(
        expected_documents
    )

    if not expected_documents:

        return True

    return bool(
        retrieved_documents
        & expected_documents
    )


def main():

    questions = load_questions()

    total = len(questions)

    retrieval_correct = 0

    print(
        f"Evaluating {total} RAG questions..."
    )

    print("=" * 70)

    for index, item in enumerate(
        questions,
        start=1,
    ):

        question = item["question"]

        expected_documents = item[
            "expected_documents"
        ]

        result = ask(
            question=question,
            user_role="admin",
            top_k=3,
        )

        source_correct = evaluate_sources(
            result["sources"],
            expected_documents,
        )

        if source_correct:
            retrieval_correct += 1

        print("\n" + "-" * 70)

        print(
            f"[{index:02d}] "
            f"{question}"
        )

        print(
            f"\nExpected answer:\n"
            f"{item['expected_answer']}"
        )

        print(
            f"\nGenerated answer:\n"
            f"{result['answer']}"
        )

        print(
            f"\nExpected documents: "
            f"{expected_documents}"
        )

        print(
            "Retrieved documents: "
            f"{[r['document_id'] for r in result['sources']]}"
        )

        print(
            f"\nRetrieval: "
            f"{'PASS' if source_correct else 'FAIL'}"
        )

    print("\n" + "=" * 70)
    print("RAG EVALUATION")
    print("=" * 70)

    print(
        f"Questions: {total}"
    )

    print(
        f"Expected source retrieved: "
        f"{retrieval_correct / total:.2%}"
    )


if __name__ == "__main__":
    main()