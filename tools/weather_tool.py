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
    # Check if running on Hugging Face Space
    is_hf_space = os.environ.get('SPACE_ID') is not None
    logger.info(f"Running on Hugging Face Space: {is_hf_space}")
    
    # Get API key from environment variable
    api_key = os.getenv('WEATHER_API_KEY')
    
    # Log environment variables for debugging (without exposing the actual key)
    env_vars = [k for k in os.environ.keys() if 'API' in k or 'KEY' in k or 'WEATHER' in k or 'HF_' in k or 'SPACE' in k]
    logger.info(f"Available environment variables that might contain API keys: {env_vars}")
    logger.info(f"API key found: {api_key is not None}")
    
    if not api_key:
        logger.warning("No WEATHER_API_KEY found in environment variables")
        raise ValueError("Weather API key not configured")
    
    # Convert unit parameter to API format
    units = "metric" if unit.lower() == "celsius" else "imperial"
    unit_symbol = "C" if unit.lower() == "celsius" else "F"
    
    # Make API request to OpenWeatherMap (you can replace with your preferred API)
    url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&units={units}&appid={api_key}"
    
    logger.info(f"Making API request to: {url.replace(api_key, 'API_KEY_HIDDEN')}")
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise exception for HTTP errors
        logger.info(f"API response status code: {response.status_code}")
    
        data = response.json()
        logger.info(f"API response data keys: {data.keys()}")
        
        temp = round(data["main"]["temp"])
        condition = data["weather"][0]["main"]
        
        logger.info(f"Successfully parsed weather data: {temp}°{unit_symbol}, {condition}")
        return f"Weather in {location}: {temp}°{unit_symbol}, {condition}"
    except Exception as e:
        logger.error(f"Error during API request or parsing: {str(e)}")
        raise

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
