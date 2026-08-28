from datetime import datetime,timedelta,timezone
import jwt
from pwdlib import PasswordHash
from app.core.config import SECRET_KEY

SECRET_KEY = SECRET_KEY

algorithm = "HS256"

access_token_expire = 60

password_hash = PasswordHash.recommended()

def hash_password(password: str)->str:
    return password_hash.hash(password)

def verify_password(password:str,hashed_password:str)->bool:
    return password_hash.verify(password,hashed_password)

def create_access_token(user_id:int,email:str,role:str):
    expires_at = (datetime.now(timezone.utc) + timedelta(minutes=access_token_expire))
    payload = {"sub":str(user_id), "email":email,"role":role,"exp":expires_at}
    
    return jwt.encode(payload,SECRET_KEY,algorithm=algorithm)

def decode_access_token(token:str):
    try:
        return jwt.decode(token,SECRET_KEY,algorithms = [algorithm])
    except jwt.InvalidTokenError:
        return None