from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import os
from dotenv import load_dotenv
from core.rate_limit import RateLimiter
from api.auth import router as auth_router
from api.moderate import router as moderate_router
from core.auth import verify_token
from db.mongodb import db

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Image Moderation API",
    description="API for detecting and blocking harmful imagery",
    version="1.0.0"
)

# Initialize rate limiter
rate_limiter = RateLimiter(requests_per_minute=60)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security bearer scheme
security = HTTPBearer()

# MongoDB connection
@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(os.getenv("MONGODB_URI", "mongodb://localhost:27017"))
    app.mongodb = app.mongodb_client[os.getenv("MONGODB_DB", "image_moderation")]

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()

# Rate limiting middleware
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    await rate_limiter.check_rate_limit(request)
    return await call_next(request)

# Error handling
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(moderate_router, prefix="/moderate", tags=["Moderation"])

@app.get("/")
async def root():
    return {"message": "Welcome to Image Moderation API"} 
