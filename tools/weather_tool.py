from typing import Dict, Any, Optional
from smolagents.tools import tool
import random
import requests
import os
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Use the basic tool decorator without parameters
@tool
def get_current_weather(location: str, unit: str = 'celsius') -> str:
    """
    Fetches the current weather for a specified location.
    
    Args:
        location (str): The location to get weather for, e.g., 'Paris, FR'
        unit (str): Temperature unit, either 'celsius' or 'fahrenheit'.
    
    Returns:
        str: A string describing the current weather conditions and temperature.
    """
    if not location:
        raise ValueError("Location is required")
        
    logger.info(f"Fetching weather for {location} in {unit}...")
    
    # Try to get real weather data from API
    try:
        return get_real_weather(location, unit)
    except Exception as e:
        logger.warning(f"Failed to get real weather data: {e}. Falling back to mock data.")
        return get_mock_weather(location, unit)

def get_real_weather(location: str, unit: str) -> str:
    """Get real weather data from a weather API"""
    # Get API key from environment variable
    api_key = os.getenv('WEATHER_API_KEY')
    
    if not api_key:
        logger.warning("No WEATHER_API_KEY found in environment variables")
        raise ValueError("Weather API key not configured")
    
    # Convert unit parameter to API format
    units = "metric" if unit.lower() == "celsius" else "imperial"
    unit_symbol = "C" if unit.lower() == "celsius" else "F"
    
    # Make API request to OpenWeatherMap (you can replace with your preferred API)
    url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&units={units}&appid={api_key}"
    
    response = requests.get(url)
    response.raise_for_status()  # Raise exception for HTTP errors
    
    data = response.json()
    temp = round(data["main"]["temp"])
    condition = data["weather"][0]["main"]
    
    return f"Weather in {location}: {temp}°{unit_symbol}, {condition}"

def get_mock_weather(location: str, unit: str) -> str:
    """Provide mock weather data as a fallback"""
    # Mock temperature in Celsius (base value)
    temp_celsius = 22
    
    # Convert temperature based on the requested unit
    if unit.lower() == 'fahrenheit':
        # Convert Celsius to Fahrenheit: (C × 9/5) + 32
        temp = round((temp_celsius * 9/5) + 32)
        unit_symbol = 'F'
    else:  # Default to Celsius
        temp = temp_celsius
        unit_symbol = 'C'
    
    # List of possible weather conditions
    conditions = ["Sunny", "Partly Cloudy", "Cloudy", "Light Rain", "Clear"]
    condition = random.choice(conditions)
    
    return f"Weather in {location}: {temp}°{unit_symbol}, {condition} (Mock Data)"
