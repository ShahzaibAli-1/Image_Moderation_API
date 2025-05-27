from fastapi import HTTPException, status, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import secrets
from datetime import datetime
from typing import Optional
from models.auth import Token

security = HTTPBearer()

def generate_token() -> str:
    """Generate a secure random token."""
    return secrets.token_urlsafe(32)

async def get_current_token(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Token:
    """Validate the bearer token and return the token object."""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = credentials.credentials
    token_doc = await request.app.mongodb.tokens.find_one({"token": token})
    
    if not token_doc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Update last used timestamp
    await request.app.mongodb.tokens.update_one(
        {"token": token},
        {"$set": {"last_used": datetime.utcnow()}}
    )
    
    return Token(**token_doc)

async def require_admin_token(token: Token = Depends(get_current_token)) -> Token:
    """Ensure the token has admin privileges."""
    if not token.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return token

async def verify_token(request: Request, token: str) -> dict:
    """Verify if a token is valid and return its data"""
    token_data = await request.app.mongodb.tokens.find_one({"token": token})
    if not token_data:
        raise HTTPException(status_code=401, detail="Invalid token")
    return token_data

async def verify_admin_token(request: Request, token: str) -> dict:
    """Verify if a token is valid and has admin privileges"""
    token_data = await verify_token(request, token)
    if not token_data.get("is_admin"):
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return token_data 
