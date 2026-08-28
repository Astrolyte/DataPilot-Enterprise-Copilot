from sqlalchemy import text

from app.core.auth import hash_password
from app.core.database import engine


def main():

    email = "hr@datapilot.local"
    password = "test12345"

    password_hash = hash_password(
        password
    )

    query = text(
        """
        UPDATE users
        SET
            email = :email,
            password_hash = :password_hash,
            is_active = TRUE
        WHERE username = 'user_1'
        """
    )

    with engine.begin() as connection:

        connection.execute(
            query,
            {
                "email": email,
                "password_hash": password_hash,
            },
        )

    print("Authentication user configured.")
    print(f"Email: {email}")
    print(f"Role: HR")


if __name__ == "__main__":
    main()