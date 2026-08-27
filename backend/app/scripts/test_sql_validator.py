from services.sql_validator import validate_sql


TEST_QUERIES = [

    # Valid
    "SELECT COUNT(*) FROM customers",

    "SELECT SUM(total_amount) "
    "FROM orders "
    "WHERE status = 'completed'",

    # Invalid
    "DELETE FROM customers",

    "DROP TABLE customers",

    "UPDATE customers "
    "SET company_name = 'Hacked'",

    # Forbidden column
    "SELECT password_hash FROM users",

    # Unknown table
    "SELECT * FROM secret_table",
]


def main():

    for sql in TEST_QUERIES:

        valid, message = validate_sql(sql)

        print("\n" + "-" * 70)

        print("SQL:")
        print(sql)

        print(
            f"\nResult: "
            f"{'PASS' if valid else 'BLOCK'}"
        )

        print(f"Message: {message}")


if __name__ == "__main__":
    main()