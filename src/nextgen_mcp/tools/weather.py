from typing import Any
import httpx
from ..middlewares.logging import logging_middleware

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "nextgen-mcp/1.0"

async def _make_nws_request(url: str) -> dict[str, Any] | None:
    headers = {"User-Agent": USER_AGENT, "Accept": "application/geo+json"}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

@logging_middleware
async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state."""
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await _make_nws_request(url)

    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."

    if not data["features"]:
        return "No active alerts for this state."

    alerts = []
    for feature in data["features"]:
        props = feature["properties"]
        alerts.append(f"Event: {props.get('event')}\nArea: {props.get('areaDesc')}\nSeverity: {props.get('severity')}\n---")
    
    return "\n".join(alerts)

@logging_middleware
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location."""
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await _make_nws_request(points_url)

    if not points_data:
        return "Unable to fetch location data."

    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await _make_nws_request(forecast_url)

    if not forecast_data:
        return "Unable to fetch forecast."

    periods = forecast_data["properties"]["periods"]
    return "\n---\n".join([f"{p['name']}: {p['detailedForecast']}" for p in periods[:5]])
