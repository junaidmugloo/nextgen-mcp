import logging
import time
from functools import wraps
from typing import Any, Callable

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("nextgen-mcp")

def logging_middleware(func: Callable) -> Callable:
    """Middleware to log tool execution time and status."""
    @wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        tool_name = func.__name__
        logger.info(f"Executing tool: {tool_name} with args: {kwargs}")
        
        try:
            result = await func(*args, **kwargs)
            duration = time.time() - start_time
            logger.info(f"Tool {tool_name} completed in {duration:.2f}s")
            return result
        except Exception as e:
            logger.error(f"Tool {tool_name} failed: {str(e)}")
            raise
            
    return wrapper
