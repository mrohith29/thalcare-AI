from utils.supabase_client import get_Supabase
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class LoginRequest(BaseModel):
    email: str
    password: str

class SignupRequest(BaseModel):
    email: str
    password: str
    user_type: str
    name: str
    phone: str

@app.post("/login")
def login(request: LoginRequest):
    supabase = get_Supabase()
    
    try:
        result = supabase.auth.sign_in_with_password({
            "email": request.email,
            "password": request.password
        })
        
        return {
            "message": "Login successful",
            "access_token": result.session.access_token,
            "user_id": result.user.id
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/signup")
def signup(request: SignupRequest):
    supabase = get_Supabase()
    
    try:
        # Sign up with Supabase Auth
        result = supabase.auth.sign_up({
            "email": request.email,
            "password": request.password
        })
        
        # Store additional user data in your users table
        user_data = {
            "id": result.user.id,
            "email": request.email,
            "user_type": request.user_type,
            "name": request.name,
            "phone": request.phone
        }
        
        supabase.table("users").insert(user_data).execute()
        
        return {
            "message": "Signup successful",
            "user_id": result.user.id
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))