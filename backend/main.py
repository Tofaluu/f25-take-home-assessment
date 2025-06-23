from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional
import uvicorn
import uuid
import os
import httpx

app = FastAPI(title="Weather Data System", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for weather data
weather_storage: Dict[str, Dict[str, Any]] = {}

class WeatherRequest(BaseModel):
    date: str
    location: str
    notes: Optional[str] = ""

class WeatherResponse(BaseModel):
    id: str

WEATHERSTACK_API_KEY = "REMOVED"

@app.post("/weather", response_model=WeatherResponse)
async def create_weather_request(request: WeatherRequest):
    """
    You need to implement this endpoint to handle the following:
    1. Receive form data (date, location, notes)
    2. Calls WeatherStack API for the location
    3. Stores combined data with unique ID in memory
    4. Returns the ID to frontend
    """
    if not WEATHERSTACK_API_KEY:
        raise HTTPException(status_code=500, detail="WeatherStack API key is not set")
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://api.weatherstack.com/current",
            params={"access_key": WEATHERSTACK_API_KEY, "query": request.location}
        )

    data = response.json()

    if "current" not in data:
        raise HTTPException(status_code=400, detail="Invalid location or API error")
    
    weather_id = str(uuid.uuid4())

    weather_storage[weather_id] = {
        "date": request.date,
        "location": request.location,
        "notes": request.notes,
        "weather": data["current"],
    }

    return WeatherResponse(id=weather_id)
    pass

@app.get("/weather/{weather_id}")
async def get_weather_data(weather_id: str):
    """
    Retrieve stored weather data by ID.
    This endpoint is already implemented for the assessment.
    """
    if weather_id not in weather_storage:
        raise HTTPException(status_code=404, detail="Weather data not found")
    
    return weather_storage[weather_id]


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)