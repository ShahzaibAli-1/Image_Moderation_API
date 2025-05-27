from fastapi import Request, HTTPException
from datetime import datetime, timedelta
from typing import Dict, Tuple
import asyncio

class RateLimiter:
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, list] = {}
        self.lock = asyncio.Lock()
    
    async def check_rate_limit(self, request: Request) -> None:
        """Check if the request should be rate limited."""
        client_ip = request.client.host
        async with self.lock:
            now = datetime.utcnow()
            minute_ago = now - timedelta(minutes=1)
            
            # Clean up old requests
            if client_ip in self.requests:
                self.requests[client_ip] = [
                    req_time for req_time in self.requests[client_ip]
                    if req_time > minute_ago
                ]
            
            # Check rate limit
            if client_ip in self.requests and len(self.requests[client_ip]) >= self.requests_per_minute:
                raise HTTPException(
                    status_code=429,
                    detail="Too many requests. Please try again later."
                )
            
            # Add new request
            if client_ip not in self.requests:
                self.requests[client_ip] = []
            self.requests[client_ip].append(now) 