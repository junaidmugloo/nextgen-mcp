import os
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from starlette.requests import Request

class ClientAuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware to validate Client ID and Client Secret for SSE transport.
    Supports both headers (X-Client-ID, X-Client-Secret) and query parameters.
    """
    async def dispatch(self, request: Request, call_next):
        # Public endpoints (health, root) are excluded
        if request.url.path in ["/", "/health"]:
            return await call_next(request)

        # Only protect MCP-related endpoints
        if request.url.path.startswith("/mcp") or request.url.path.startswith("/sse"):
            expected_id = os.getenv("CLIENT_ID")
            expected_secret = os.getenv("CLIENT_SECRET")
            
            # If credentials are not set in environment, allow all (no auth)
            if not expected_id or not expected_secret:
                return await call_next(request)

            # Check headers
            request_id = request.headers.get("X-Client-ID") or request.query_params.get("client_id")
            request_secret = request.headers.get("X-Client-Secret") or request.query_params.get("client_secret")
            
            if request_id != expected_id or request_secret != expected_secret:
                return JSONResponse(
                    {
                        "error": "Unauthorized",
                        "message": "Invalid or missing Client ID/Secret. Please provide 'X-Client-ID' and 'X-Client-Secret' headers."
                    },
                    status_code=401
                )
        
        return await call_next(request)
