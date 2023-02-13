import requests
import os
from uvicorn import run
from fastapi import UploadFile, File, FastAPI

owm_api_key = "5f1d3a5a193fe9ed245cd087ddc305a9"
app = FastAPI()

@app.get("/")
async def root():
    return "Welcome to the Weather API!"

@app.post("/weather")
async def get_weather(request: dict):
    """"Handles POST request w/ embedded lat/lon"""
    lat = request.get("lat")
    lon = request.get("lon")
    weather_response = requests.get(f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely&appid={owm_api_key}&units=imperial")
    return weather_response.json()
if __name__ == "__main__":
   port = int(os.environ.get('PORT', 5000))
   run(app, host="0.0.0.0", port=port)