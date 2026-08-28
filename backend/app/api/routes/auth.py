from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr

from app.core.auth import (hash_password,verify_password,create_access_token)
from app.services.user_service import (get_user_by_email,create_user)

router = APIRouter(prefix="/auth",tags=["Authentication"])

class RegisterRequest(BaseModel):
    email: EmailStr
    name : str
    password: str
    
class LoginRequest(BaseModel):
    
    email: EmailStr
    password: str
    
    
@router.post("/register")
def register(request: RegisterRequest):
    existing_user = get_user_by_email(request.email)
    if existing_user:
        raise HTTPException(status_code = 409, detail = "User already exists")
    
    if len(request.password)< 8:
        raise HTTPException(status_code = 400, detail = "password must atleast be 8 Characters long")
        
    user = create_user(email = request.email, username = request.name, password_hash = hash_password(request.password), role="SALES")
    
    token = create_access_token(user_id=user["user_id"],email=user["email"],role = user["role"])
    
    return {
        "access_token":token,
        "token_type":"bearer",
        "user":user
    }    
    
@router.post("/login")
def login(request: LoginRequest):
    user = get_user_by_email(request.email)
    
    if not user:
        raise HTTPException(
            status_code = 401,
            detail = "Invalid Email or Password"
        )
        
    if not user["password_hash"]:
        raise HTTPException(
            status_code = 401,
            detail = "Password login is not enabled for this account"
        )
        
    if not verify_password(request.password, user["password_hash"]):
        raise HTTPException(
            status_code = 401,
            detail = "Invalid Email pr Password"
        )
    
    if not user["is_active"]:
        raise HTTPException(
            status_code = 401,
            detail = "Account is disabled"
        )
        
    token = create_access_token(user_id = user["user_id"],email = user["email"],role = user["role"])
    
    return {
        "access_token" : token,
        "type": "Bearer",
        "user": {
            "user_id":user["user_id"],
            "email":user["email"],
            "username":user["username"],
            "role":user["role"],
        }
    }