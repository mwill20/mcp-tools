from typing import Dict, Any, Optional
from smolagents.tools import tool

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
    # TODO: Implement API call to weather service
    return f"Weather in {location}: 22°{unit[0].upper()}, Sunny"  # Mock response
