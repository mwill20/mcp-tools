import os
import sys
import json
import logging
import requests
import gradio as gr
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def check_environment():
    """Check environment variables and return diagnostic info"""
    # Check if running on Hugging Face Space
    is_hf_space = os.environ.get('SPACE_ID') is not None
    
    # Get API key (safely)
    api_key = os.environ.get('WEATHER_API_KEY')
    api_key_status = "Found" if api_key else "Not found"
    
    # Get environment variables that might be relevant
    env_vars = [k for k in os.environ.keys() 
                if 'API' in k or 'KEY' in k or 'WEATHER' in k 
                or 'HF_' in k or 'SPACE' in k]
    
    # Check if requests package is available
    requests_version = requests.__version__ if 'requests' in sys.modules else "Not installed"
    
    # Directory info
    try:
        current_dir = os.getcwd()
        dir_contents = os.listdir('.')
    except Exception as e:
        current_dir = str(e)
        dir_contents = []
    
    # Return diagnostic info
    return {
        "Running on Hugging Face Space": is_hf_space,
        "WEATHER_API_KEY status": api_key_status,
        "API key length (if found)": len(api_key) if api_key else 0,
        "Python version": sys.version,
        "Requests version": requests_version,
        "Current directory": current_dir,
        "Directory contents": dir_contents,
        "Environment variables that might contain API keys": env_vars,
        "All environment variables (names only)": list(os.environ.keys())
    }

def test_api_call(location="London,UK", unit="metric"):
    """Test the OpenWeatherMap API call directly"""
    api_key = os.environ.get('WEATHER_API_KEY')
    
    if not api_key:
        return {
            "status": "error",
            "message": "No API key found in environment variables",
            "environment_check": check_environment()
        }
    
    try:
        # Make API request
        url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&units={unit}&appid={api_key}"
        response = requests.get(url, timeout=10)
        
        # Check response
        if response.status_code == 200:
            data = response.json()
            return {
                "status": "success",
                "response_code": response.status_code,
                "data": data,
                "environment_check": check_environment()
            }
        else:
            return {
                "status": "error",
                "response_code": response.status_code,
                "message": response.text,
                "environment_check": check_environment()
            }
    except Exception as e:
        return {
            "status": "exception",
            "message": str(e),
            "environment_check": check_environment()
        }

# Create Gradio interface
with gr.Blocks(title="API Debug Tool") as demo:
    gr.Markdown("# Weather API Debug Tool")
    
    with gr.Tab("Environment Check"):
        check_btn = gr.Button("Check Environment")
        env_output = gr.JSON(label="Environment Information")
        check_btn.click(fn=check_environment, inputs=None, outputs=env_output)
    
    with gr.Tab("Test API Call"):
        with gr.Row():
            location = gr.Textbox(label="Location", value="London,UK")
            unit = gr.Radio(["metric", "imperial"], label="Units", value="metric")
        test_btn = gr.Button("Test API Call")
        api_output = gr.JSON(label="API Response")
        test_btn.click(fn=test_api_call, inputs=[location, unit], outputs=api_output)

if __name__ == "__main__":
    # Launch the app
    demo.launch(server_name="0.0.0.0", server_port=7861)
