from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.auth import decode_access_token
from app.services.user_service import get_user_by_email, get_user_by_id

security = HTTPBearer()
# oauth_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    
    token = credentials.credentials
    
    payload = decode_access_token(token)
    
    if not payload:
        print("There's no payload")
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )
    
    email = payload.get("email")
    
    if not email:
        print("email not found")
        raise HTTPException(
            status_code=401,
            detail="Invalid Authentication token"
        )
    user_id = payload.get("sub")
    
    if not user_id:
        print("User_id not found")
        raise HTTPException(
            status_code=401,
            detail="User ID missing from Token"
        )
    
    user = get_user_by_id(user_id)
    if not user:
        print("user not found")
        raise HTTPException(
            status_code=401,
            detail="Invalid User or User not found"
        )
        
    if not user["is_active"]:
        raise HTTPException(
            status_code=401,
            detail="User is deactivated"
        )
    
    return user;
    
