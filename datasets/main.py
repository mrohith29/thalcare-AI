"""
    Design a FastAPI endpoint that   :

    Accepts a POST request with a JSON payload containing:
        Email (must be valid)
        Age (must be a positive integer)
        Username (must be an alphanumeric string with at least 5 characters)
    
    If all validations pass, 
    
    return:
        json
        { 
            "status": "success", 
            "message": "Valid input data." 
        }

"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
import re

app = FastAPI(title="Validate JSON Payload")

@app.post('/validation')
def validate_data(data: dict):
    email = data.get('email')
    age = data.get('age')
    user_name = data.get('username')

    if not (email and age and user_name):
        return JSONResponse(content= {"status": "error", "message": "Invalid data"})
    
    email_re = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(email_re, email):
        return JSONResponse(content= {"status": "error", "message": "Invalid Email"})
    
    if age < 1:
        return JSONResponse(content= {"status": "error", "message": "Invalid Age"})
    
    username_re = r'^[a-zA-Z0-9]{5,}$'
    if not re.match(username_re, user_name):
        return JSONResponse(content= {"status": "error", "message": "Invalid Username"})
    
    return JSONResponse(content= {"status": "success", "message": "Valid input data."})


@app.get('/name/{name}')
def get_name(name: str):
    return f"Hello {name}!"