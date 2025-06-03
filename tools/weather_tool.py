from typing import Dict, Any, Optional
from smolagents.tools import tool
import random

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
        
    print(f"Fetching weather for {location} in {unit}...")
    
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
    
    return f"Weather in {location}: {temp}°{unit_symbol}, {condition}"
