from ..middlewares.logging import logging_middleware

@logging_middleware
async def greet_user(name: str) -> str:
    """A friendly greeting tool to demonstrate the boilerplate."""
    return f"Hii {name} this tool is developed by junaid mugloo for easy use of mcp boilerplate"
