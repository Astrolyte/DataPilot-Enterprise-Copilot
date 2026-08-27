from app.services.sql_generator import generate_sql
from app.services.sql_executor import execute_sql
from app.services.sql_repair import repair_sql

MAX_RETRIES = 2

def ask_sql(question: str):
    
    sql = generate_sql(question)
    
    for attempt in range(MAX_RETRIES + 1):

        try:

            rows = execute_sql(sql)

            return {
                "question": question,
                "sql": sql,
                "rows": rows,
                "attempts": attempt + 1,
            }

        except Exception as error:

            if attempt >= MAX_RETRIES:
                raise

            sql = repair_sql(
                question=question,
                sql=sql,
                error=str(error),
            )