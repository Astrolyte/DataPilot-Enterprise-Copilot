from sqlalchemy import text
from app.core.database import engine

def get_user_by_email(email:str):
    
    query = text(
        """
            SELECT
                user_id,
                email,
                username,
                password_hash,
                google_sub,
                role,
                is_active
            FROM users
            WHERE email = :email
            LIMIT 1
        """
    )
    
    with engine.connect() as connection:
        
        row = (connection.execute(
            query,
            {
                "email":email,
            }
        ).mappings().first())
        
        return dict(row) if row else None

def get_user_by_id(user_id: int):
    query = text(
        """
        SELECT 
            user_id,
            email,
            username,
            password_hash,
            google_sub,
            role,
            is_active
        FROM users
        WHERE user_id = :user_id
        LIMIT 1
                
        """
    )
    
    with engine.connect() as connection:
        row = (
            connection.execute(
                query,
                {
                    "user_id":user_id,
                }
            ).mappings().first()
        )
    return dict(row) if row else None
    
def get_user_by_google_sub(google_sub: str):

    query = text(
        """
        SELECT
            user_id,
            email,
            username,
            password_hash,
            google_sub,
            role,
            is_active
        FROM users
        WHERE google_sub = :google_sub
        LIMIT 1
        """
    )

    with engine.connect() as connection:

        row = (
            connection.execute(
                query,
                {
                    "google_sub": google_sub,
                },
            ).mappings().first()
        )

    return dict(row) if row else None

def create_user(email: str,username: str,password_hash: str | None = None,google_sub: str | None = None,role: str = "sales",):

    query = text(
        """
        INSERT INTO users (
            email,
            username,
            password_hash,
            google_sub,
            role
        )
        VALUES (
            :email,
            :username,
            :password_hash,
            :google_sub,
            :role
        )
        RETURNING
            user_id,
            email,
            username,
            role
        """
    )

    with engine.begin() as connection:

        row = (
            connection.execute(
                query,
                {
                    "email": email,
                    "username": username,
                    "password_hash": password_hash,
                    "google_sub": google_sub,
                    "role": role,
                },
            )
            .mappings()
            .first()
        )

    return dict(row)

def link_google_account(user_id:int,google_sub:str):
    query = text(
        """
        UPDATE users
        SET google_sub = :google_sub
        WHERE user_id = :user_id
        RETURNING
            user_id,
            email,
            username,
            role,
            is_active
        """
    )
    with engine.begin() as connection:
        
        row = (
            connection.execute(
                query,
                {
                    "user_id":user_id,
                    "google_sub":google_sub
                }
            ).mappings().first()
        )
        return dict(row) if row else None
    
def username_exists(username: str) -> bool:

    query = text(
        """
        SELECT 1
        FROM users
        WHERE username = :username
        LIMIT 1
        """
    )

    with engine.connect() as connection:

        row = connection.execute(
            query,
            {"username": username},
        ).first()

    return row is not None

def generate_unique_username(name: str) -> str:

    base_username = name.strip().replace(" ", "_")

    username = base_username
    counter = 1

    while username_exists(username):

        username = f"{base_username}_{counter}"
        counter += 1

    return username
