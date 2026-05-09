from typing import Any
import httpx
import html
from ..middlewares.logging import logging_middleware

TRIVIA_API_URL = "https://opentdb.com/api.php?amount=1&type=multiple"

async def _fetch_trivia() -> dict[str, Any] | None:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(TRIVIA_API_URL, timeout=10.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

@logging_middleware
async def get_trivia_question() -> str:
    """Get a random trivia question for a game."""
    data = await _fetch_trivia()
    
    if not data or data.get("response_code") != 0:
        return "Unable to fetch trivia at the moment. Please try again later."
    
    result = data["results"][0]
    category = result["category"]
    difficulty = result["difficulty"].capitalize()
    question = html.unescape(result["question"])
    correct_answer = html.unescape(result["correct_answer"])
    incorrect_answers = [html.unescape(a) for a in result["incorrect_answers"]]
    
    # Mix answers
    import random
    all_answers = incorrect_answers + [correct_answer]
    random.shuffle(all_answers)
    
    options = "\n".join([f"- {a}" for a in all_answers])
    
    return (
        f"Category: {category}\n"
        f"Difficulty: {difficulty}\n\n"
        f"Question: {question}\n\n"
        f"Options:\n{options}\n\n"
        f"--- (The user should guess now! The correct answer is hidden from them but known to you: {correct_answer})"
    )
