import json
from pathlib import Path

from services.retriever import retrieve

EVAL_file = Path("data/evaluation/eval.json")

def load_questions():
    
    with EVAL_file.open(
        "r",
        encoding="utf-8"
    ) as file:
        
        return json.load(file)
    
def recall_at_k(retrieved_documents,expected_documents,k):
    
    top_k = retrieved_documents[:k]
    
    return int(any(
        document in expected_documents
        for document in top_k))
    
    
def main():
    
    questions = load_questions()
    
    total = len(questions)
    
    recall_1 = 0
    recall_3 = 0
    recall_5 = 0
    
    print(f"evaluation {total} retrieval questions...")
    
    for index,item in enumerate(questions,start = 1):
        
        question = item["question"]
        expected = set(item["expected_documents"])
        
        results = retrieve(query = question,user_role="admin",top_k=5)
        retrieved = [
            result["document_id"]
            for result in results         
                     ]
        r1 = recall_at_k(retrieved,expected,1)
        r3 = recall_at_k(retrieved,expected,3)
        r5 = recall_at_k(retrieved,expected,5)
        
        recall_1 += r1
        recall_3 += r3
        recall_5 += r5

        print(f"Question: {question}")

        print(f"Expected: {list(expected)}")

        print(f"Retrieved: {retrieved}" )
        
        print(
            f"R@1: {'PASS' if r1 else 'FAIL'}"
            f"  |  "
            f"R@3: {'PASS' if r3 else 'FAIL'}"
            f"  |  "
            f"R@5: {'PASS' if r5 else 'FAIL'}"
            f"  |  "
        )

    print("\n" + "=" * 70)
    print("RETRIEVAL EVALUATION")
    print("=" * 70)

    print(f"Recall@1: "
        f"{recall_1 / total:.2%}"
    )

    print(f"Recall@3: "
        f"{recall_3 / total:.2%}"
    )

    print(
        f"Recall@5: "
        f"{recall_5 / total:.2%}"
    )

if __name__ == "__main__":
    main()