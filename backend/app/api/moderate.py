from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime
import tensorflow as tf
import numpy as np
from PIL import Image
import io

from core.auth import verify_token
from db.mongodb import db
from services.image_analyzer import analyze_image

router = APIRouter()
security = HTTPBearer()

ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/gif"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

@router.post("")
async def moderate_image(
    file: UploadFile = File(...),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Analyze an uploaded image for harmful content.
    Returns a safety report with confidence scores for various categories.
    """
    # Verify token
    token_data = await verify_token(credentials.credentials)
    
    # Validate file type
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed types: {', '.join(ALLOWED_MIME_TYPES)}"
        )
    
    # Read and validate file size
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds maximum allowed size of {MAX_FILE_SIZE/1024/1024}MB"
        )
    
    try:
        # Convert to PIL Image
        image = Image.open(io.BytesIO(contents))
        
        # Analyze image
        analysis_result = await analyze_image(image)
        
        # Record usage
        await db.usages.insert_one({
            "token": token_data["token"],
            "endpoint": "moderate",
            "timestamp": datetime.utcnow(),
            "file_size": len(contents),
            "file_type": file.content_type
        })
        
        return analysis_result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
