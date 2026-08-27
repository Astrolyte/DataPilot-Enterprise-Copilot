import sqlglot
from sqlglot import exp


ALLOWED_TABLES = {
    "employees",
    "customers",
    "products",
    "orders",
    "order_items",
    "transactions",
    "customer_contracts",
}


FORBIDDEN_COLUMNS = {
    "password_hash",
}


def validate_sql(sql: str):

    sql = sql.strip()

    if not sql:
        return False, "Empty SQL query."

    # Parse SQL using PostgreSQL dialect
    try:
        statements = sqlglot.parse(
            sql,
            read="postgres",
        )
    except Exception as e:
        return False, f"Invalid SQL syntax: {e}"

    # Only one statement is allowed
    if len(statements) != 1:
        return False, "Only one SQL statement is allowed."

    statement = statements[0]

    # Only SELECT statements are allowed
    if not isinstance(statement, exp.Select):
        return False, (
            "Only SELECT queries are allowed."
        )

    # Check tables
    tables = statement.find_all(exp.Table)

    for table in tables:

        table_name = table.name.lower()

        if table_name not in ALLOWED_TABLES:
            return False, (
                f"Table '{table_name}' "
                f"is not allowed."
            )

    # Check forbidden columns
    columns = statement.find_all(exp.Column)

    for column in columns:

        column_name = column.name.lower()

        if column_name in FORBIDDEN_COLUMNS:
            return False, (
                f"Access to column "
                f"'{column_name}' is forbidden."
            )

    return True, "SQL is valid."