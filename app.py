import os
import sys
import logging
import gradio as gr
from textblob import TextBlob
from dotenv import load_dotenv
from tools import get_current_weather, simple_calculator

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("mcp_app.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Get server configuration from environment variables
# Use environment variables for Hugging Face Spaces
HF_SPACE = os.environ.get('SPACE_ID') is not None

# If running on Hugging Face Space, ensure API keys are properly set
if HF_SPACE:
    logger.info("Running on Hugging Face Space")
    # Log available environment variables for debugging (without exposing actual keys)
    env_vars = [k for k in os.environ.keys() if 'API' in k or 'KEY' in k or 'WEATHER' in k or 'HF_' in k or 'SPACE' in k]
    logger.info(f"Available environment variables that might contain API keys: {env_vars}")
    
    # Check if WEATHER_API_KEY is available
    weather_api_key = os.environ.get('WEATHER_API_KEY')
    logger.info(f"WEATHER_API_KEY found: {weather_api_key is not None}")
    
    # Ensure the key is available to the weather tool
    if weather_api_key:
        os.environ['WEATHER_API_KEY'] = weather_api_key
        logger.info("Successfully set WEATHER_API_KEY in environment")

# Server configuration
if HF_SPACE:
    # Configuration for Hugging Face Spaces
    SERVER_NAME = '0.0.0.0'
    SERVER_PORT = 7860
    MCP_SERVER = False  # Disable MCP in Hugging Face for now
    
    # Log more details about the environment
    logger.info(f"Hugging Face Space ID: {os.environ.get('SPACE_ID')}")
    logger.info(f"Hugging Face Space Name: {os.environ.get('SPACE_NAME')}")
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Current directory: {os.getcwd()}")
    logger.info(f"Directory contents: {os.listdir('.')}")
else:
    # Local development configuration
    SERVER_NAME = os.getenv('SERVER_NAME', '0.0.0.0')
    SERVER_PORT = int(os.getenv('SERVER_PORT', '7860'))
    MCP_SERVER = os.getenv('MCP_SERVER', 'True').lower() == 'true'

from smolagents.tools import tool

@tool
def sentiment_analysis(text: str) -> dict:
    """
    Performs sentiment analysis on the input text.

    Args:
        text (str): The text to analyze.

    Returns:
        dict: A dictionary containing polarity, subjectivity, and a qualitative assessment.
    """
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity

    if polarity > 0.1:
        assessment = "positive"
    elif polarity < -0.1:
        assessment = "negative"
    else:
        assessment = "neutral"

    return {
        "polarity": polarity,
        "subjectivity": subjectivity,
        "assessment": assessment
    }

def weather_interface(location: str, unit: str) -> str:
    """Gradio interface function for weather tool"""
    try:
        result = get_current_weather(location=location, unit=unit)
        logger.info(f"Weather result: {result}")
        return result
    except Exception as e:
        error_msg = f"Error getting weather: {str(e)}"
        logger.error(error_msg)
        return f"Error: {error_msg} (Mock Data will be used next time)"

def calculator_interface(operand1: float, operand2: float, operation: str) -> float:
    """Gradio interface function for calculator tool"""
    return simple_calculator(operand1, operand2, operation)

# Create tabbed interface
with gr.Blocks(title="MCP Tools") as demo:
    gr.Markdown("# MCP Tools Dashboard")
    
    with gr.Tab("Sentiment Analysis"):
        with gr.Row():
            text_input = gr.Textbox(
                lines=3, 
                placeholder="Enter text for sentiment analysis...",
                label="Input Text"
            )
        analyze_btn = gr.Button("Analyze Sentiment")
        sentiment_output = gr.JSON(label="Analysis Results")
        analyze_btn.click(
            fn=sentiment_analysis,
            inputs=text_input,
            outputs=sentiment_output
        )
    
    with gr.Tab("Weather Tool"):
        with gr.Row():
            location = gr.Textbox(label="Location", placeholder="e.g., Paris, FR")
            unit = gr.Radio(
                ["celsius", "fahrenheit"], 
                label="Temperature Unit", 
                value="celsius"
            )
        weather_btn = gr.Button("Get Weather")
        weather_output = gr.Textbox(label="Weather Information")
        
        # Add debug information for Hugging Face Space
        if HF_SPACE:
            with gr.Accordion("Debug Info", open=False):
                debug_info = gr.Textbox(
                    value=f"Running on Hugging Face Space: {HF_SPACE}\n" +
                          f"API Key configured: {os.environ.get('WEATHER_API_KEY') is not None}\n" +
                          f"Space ID: {os.environ.get('SPACE_ID')}\n" +
                          f"Python version: {sys.version}",
                    label="Environment Information",
                    interactive=False
                )
        weather_btn.click(
            fn=weather_interface,
            inputs=[location, unit],
            outputs=weather_output
        )
        
        # Add example queries
        gr.Examples(
            examples=[
                ["London, UK", "celsius"],
                ["New York, US", "fahrenheit"],
                ["Tokyo, JP", "celsius"],
                ["Sydney, AU", "celsius"],
            ],
            inputs=[location, unit],
        )
    
    with gr.Tab("Calculator"):
        with gr.Row():
            with gr.Column():
                operand1 = gr.Number(label="First Number")
                operand2 = gr.Number(label="Second Number")
                operation = gr.Dropdown(
                    ["add", "subtract", "multiply", "divide"],
                    label="Operation",
                    value="add"
                )
                calc_btn = gr.Button("Calculate")
            result = gr.Number(label="Result")
            
        calc_btn.click(
            fn=calculator_interface,
            inputs=[operand1, operand2, operation],
            outputs=result
        )

# MCP tools to expose - all are already decorated with @tool

if __name__ == "__main__":
    logger.info(f"Starting server on http://{SERVER_NAME}:{SERVER_PORT}")
    
    # Configure MCP endpoints if enabled
    if MCP_SERVER:
        logger.info("MCP Server: Enabled")
        try:
            # In Gradio 5.32.0, MCP endpoints are automatically created for functions
            # decorated with @tool from smolagents.tools
            logger.info("MCP endpoints will be automatically created for @tool decorated functions")
            
            # Launch with MCP support
            logger.info("Launching Gradio with MCP support...")
            demo.launch(
                server_name=SERVER_NAME,
                server_port=SERVER_PORT,
                debug=True,
                show_error=True
            )
            logger.info("Launched with MCP support.")
            logger.info(f"MCP endpoints available at: http://{SERVER_NAME}:{SERVER_PORT}/mcp/tools/{{tool_name}}/call")
        except Exception as e:
            logger.error(f"Failed to launch with MCP: {e}")
            import traceback
            logger.error(traceback.format_exc())
            logger.info("Falling back to standard launch without MCP.")
            
            # Standard launch without MCP
            logger.info("Launching Gradio without MCP...")
            demo.launch(
                server_name=SERVER_NAME,
                server_port=SERVER_PORT,
                debug=True,
                show_error=True
            )
    else:
        # Standard launch without MCP
        logger.info("MCP Server: Disabled by configuration.")
        logger.info("Launching Gradio without MCP...")
        demo.launch(
            server_name=SERVER_NAME,
            server_port=SERVER_PORT,
            debug=True,
            show_error=True
        )
