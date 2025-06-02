import sys
import importlib.util
from pathlib import Path

def test_mcp_tools():
    """Test if MCP tools are properly decorated and accessible."""
    print("Testing MCP tools...")
    
    # Test if smolagents is installed
    try:
        import smolagents
        print(f"✓ smolagents is installed (version: {smolagents.__version__})")
    except ImportError:
        print("✗ smolagents is not installed")
        return False
    
    # Test if gradio is installed
    try:
        import gradio as gr
        print(f"✓ gradio is installed (version: {gr.__version__})")
    except ImportError:
        print("✗ gradio is not installed")
        return False
    
    # Test if we can import the tools
    try:
        from tools import get_current_weather, simple_calculator
        print("✓ Successfully imported tools")
    except ImportError as e:
        print(f"✗ Failed to import tools: {e}")
        return False
    
    # Test if the tools are properly decorated
    try:
        # Check if the tools have the expected attributes from @tool decoration
        print("Checking get_current_weather attributes:")
        for attr in dir(get_current_weather):
            if 'tool' in attr.lower():
                print(f"  - {attr}")
                
        print("\nChecking simple_calculator attributes:")
        for attr in dir(simple_calculator):
            if 'tool' in attr.lower():
                print(f"  - {attr}")
    except Exception as e:
        print(f"✗ Error checking tool attributes: {e}")
        return False
    
    # Test sentiment_analysis function
    try:
        # Import the sentiment_analysis function from app.py
        app_path = Path(__file__).parent / "app.py"
        spec = importlib.util.spec_from_file_location("app", app_path)
        app = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(app)
        
        print("\nChecking sentiment_analysis attributes:")
        for attr in dir(app.sentiment_analysis):
            if 'tool' in attr.lower():
                print(f"  - {attr}")
    except Exception as e:
        print(f"✗ Error checking sentiment_analysis: {e}")
        return False
    
    print("\nAll tests completed.")
    return True

if __name__ == "__main__":
    success = test_mcp_tools()
    print(f"\nTest result: {'SUCCESS' if success else 'FAILURE'}")
    sys.exit(0 if success else 1)
