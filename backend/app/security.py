import os
from fastapi import Header, HTTPException, status

def verify_api_key(authorization: str = Header(...)):
    api_key = os.getenv("ADMIN_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="Admin API key not set")
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid Authorization header")
    token = authorization.split(" ", 1)[1]
    if token != api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")
    return token
