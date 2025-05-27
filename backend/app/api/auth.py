from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime
import secrets
from typing import List

from core.auth import verify_admin_token
from models.auth import Token, TokenCreate

router = APIRouter()
security = HTTPBearer()

@router.post("/tokens", response_model=Token)
async def create_token(
    request: Request,
    token_data: TokenCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Create a new token (admin only)"""
    await verify_admin_token(request, credentials.credentials)
    
    token = {
        "token": secrets.token_urlsafe(32),
        "is_admin": token_data.is_admin,
        "created_at": datetime.utcnow()
    }
    
    await request.app.mongodb.tokens.insert_one(token)
    return token

@router.get("/tokens", response_model=List[Token])
async def list_tokens(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """List all tokens (admin only)"""
    await verify_admin_token(request, credentials.credentials)
    
    tokens = await request.app.mongodb.tokens.find().to_list(length=None)
    return tokens

@router.delete("/tokens/{token}")
async def delete_token(
    request: Request,
    token: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Delete a specific token (admin only)"""
    await verify_admin_token(request, credentials.credentials)
    
    result = await request.app.mongodb.tokens.delete_one({"token": token})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Token not found")
    
    return {"message": "Token deleted successfully"} 
