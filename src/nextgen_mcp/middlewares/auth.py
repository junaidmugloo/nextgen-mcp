import os
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from starlette.requests import Request

class APIKeyMiddleware(BaseHTTPMiddleware):
    """
    Middleware to validate API keys for SSE transport.
    Supports both 'X-API-Key' header and 'api_key' query parameter.
    """
    async def dispatch(self, request: Request, call_next):
        # Public endpoints (health, root) are excluded
        if request.url.path in ["/", "/health"]:
            return await call_next(request)

        # Only protect MCP-related endpoints
        if request.url.path.startswith("/mcp") or request.url.path.startswith("/sse"):
            api_key = os.getenv("API_KEY")
            
            # If API_KEY is not set in environment, allow all (no auth)
            if not api_key:
                return await call_next(request)

            # Check header and query parameters
            request_key = request.headers.get("X-API-Key") or request.query_params.get("api_key")
            
            if request_key != api_key:
                return JSONResponse(
                    {
                        "error": "Unauthorized",
                        "message": "Invalid or missing API Key. Please provide 'X-API-Key' header or 'api_key' query parameter."
                    },
                    status_code=401
                )
        
        return await call_next(request)
