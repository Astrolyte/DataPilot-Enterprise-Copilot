from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from urllib.parse import urlencode, quote
import secrets
import httpx
import json
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests


from app.core.config import (GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI, FRONTEND_URL)
from app.core.auth import (hash_password,verify_password,create_access_token)
from app.services.user_service import (get_user_by_email,create_user,get_user_by_id,get_user_by_google_sub,link_google_account, username_exists,generate_unique_username)

router = APIRouter(prefix="/auth",tags=["Authentication"])

class RegisterRequest(BaseModel):
    email: EmailStr
    name : str
    password: str
    
# class LoginRequest(BaseModel):
    
#     email: EmailStr
#     password: str
    
    
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
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user_by_email(form_data.username)
    
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
        
    if not verify_password(form_data.password, user["password_hash"]):
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

@router.get("/google/login")
def google_login():
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "response_type":"code",
        "scope":"openid email profile",
        "access_type":"offline",
        "prompt":"select_account"
    }
    
    google_url = "https://accounts.google.com/o/oauth2/v2/auth?" + urlencode(params)
    
    return RedirectResponse(google_url)

@router.get("/google/callback")
async def google_callback(code:str):
    
    async with httpx.AsyncClient() as client:

        token_response = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "redirect_uri": GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
            },
        )
        token_data = token_response.json()
        
        if token_response.status_code != 200:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Google token exchange failed",
                    "details": token_data,
                },
            )
            
        google_token = token_data.get("id_token")
        
        if not google_token:
            raise HTTPException(
                status_code=400,
                detail="Google did not return an ID token",
            )
            
        try: 
            google_user = id_token.verify_oauth2_token(google_token,google_requests.Request(),GOOGLE_CLIENT_ID)
        except ValueError as e:
            print("GOOGLE TOKEN ERROR:", repr(e))
        
            raise HTTPException(
                status_code=401,
                detail="Invalid Google Token"
            )
        
        google_sub = google_user["sub"]
        email = google_user["email"]
        name = google_user.get("name",email.split("@")[0])
        
        #finding user by google identity first
        user = get_user_by_google_sub(google_sub)
        
        #then checking by email
        if not user:
            user = get_user_by_email(email)
            
            if user:
                user = link_google_account(user["user_id"],google_sub)
                
        if not user:
            username = generate_unique_username(name)
            user = create_user(
                email = email,
                username = username,
                google_sub=google_sub,
                role = "SALES"
            )
        token = create_access_token(
                user_id=user["user_id"],
                email=user["email"],
                role=user["role"]
        )
        
        # Build callback URL with properly URL-encoded parameters
        callback_params = urlencode({
            "token": token,
            "email": user["email"],
            "username": user["username"],
            "user_id": user["user_id"],
            "role": user["role"],
        })
        callback_url = f"{FRONTEND_URL}/auth/callback?{callback_params}"
        
        print(f"[GOOGLE AUTH] Frontend URL: {FRONTEND_URL}")
        print(f"[GOOGLE AUTH] Callback URL: {callback_url}")
        
        # Use HTML response with JavaScript for more reliable client-side redirect
        # Using JSON.stringify to safely encode the URL
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Redirecting...</title>
            <meta charset="utf-8">
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", "Oxygen", "Ubuntu", "Cantarell", sans-serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                }}
                .container {{
                    text-align: center;
                    color: white;
                }}
                .spinner {{
                    border: 4px solid rgba(255, 255, 255, 0.3);
                    border-top: 4px solid white;
                    border-radius: 50%;
                    width: 40px;
                    height: 40px;
                    animation: spin 1s linear infinite;
                    margin: 0 auto 20px;
                }}
                @keyframes spin {{
                    0% {{ transform: rotate(0deg); }}
                    100% {{ transform: rotate(360deg); }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="spinner"></div>
                <p>Signing you in to DataPilot...</p>
            </div>
            <script>
                // Safely redirect using JSON-encoded URL
                const redirectUrl = {json.dumps(callback_url)};
                window.location.href = redirectUrl;
                
                // Fallback timeout
                setTimeout(function() {{
                    if (window.location.href === redirectUrl) {{
                        alert('Redirect failed. Please try again or copy this URL manually: ' + redirectUrl);
                    }}
                }}, 5000);
            </script>
        </body>
        </html>
        """
        return HTMLResponse(content=html_content)