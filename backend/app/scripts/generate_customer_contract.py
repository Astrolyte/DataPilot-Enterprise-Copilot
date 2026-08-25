from pathlib import Path
from sqlalchemy import text
from app.core.database import engine

DOCS_DIR = Path("data/contracts")
NUM_CONTRACT_DOCS = 50

def generate_contract_docs(connection):
    DOCS_DIR.mkdir(parents = True,exist_ok=True)
    
    rows = connection.execute(
        text(
             """SELECT
                c.customer_id,
                c.company_name,
                c.customer_segment,
                cc.contract_id,
                cc.contract_type,
                cc.refund_window_days,
                cc.document_id,
                cc.signed_date,
                cc.annual_value

            FROM customers c

            JOIN customer_contracts cc
                ON c.customer_id = cc.customer_id

            ORDER BY cc.annual_value DESC

            LIMIT :limit
            """
        ),{
            "limit":NUM_CONTRACT_DOCS
        }
    ).mappings().all()
    
    for row in rows:

        content = f"""[document_id: {row['document_id']}]
[department: finance]
[allowed_roles: finance,sales,admin]
[customer_id: {row['customer_id']}]
[document_type: contract]

Customer Contract — {row['company_name']}

Customer: {row['company_name']}
Customer ID: {row['customer_id']}
Customer segment: {row['customer_segment']}

Contract type: {row['contract_type']}
Contract signed: {row['signed_date']}
Annual contract value: ${row['annual_value']:,.2f}

Refund Terms

This contract entitles {row['company_name']} to a
refund window of {row['refund_window_days']} days from
the date of purchase, in accordance with AcmeCloud's
{row['contract_type']} contract terms.

The refund window specified in this agreement takes
precedence over general AcmeCloud refund policies where
the two differ.

This document is the authoritative source for
{row['company_name']}'s specific contractual terms.
"""

        file_path = (DOCS_DIR / f"{row['document_id']}.txt")
        file_path.write_text(content.strip() + "\n",encoding = "utf-8")
    
    print(f"generated {len(rows)} contract documents in {DOCS_DIR}/")
    
    return len(rows)


def main():
    with engine.connect() as connection:
        generate_contract_docs(connection)
        
        
if __name__ == "__main__":
    main()