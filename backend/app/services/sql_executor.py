from sqlalchemy import text

from app.core.database import engine
from app.services.sql_validator import validate_sql

def execute_sql(sql: str):

    # 1. Validate generated SQL
    is_valid, message = validate_sql(sql)

    if not is_valid:
        raise ValueError(f"SQL validation failed: {message}")

    # 2. Execute read-only query
    with engine.connect() as connection:

        result = connection.execute(text(sql))

        # Convert SQLAlchemy rows into dictionaries
        rows = [
            dict(row._mapping)
            for row in result
        ]

    return rows