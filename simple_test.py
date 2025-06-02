print("Starting simple test...")

try:
    print("Importing smolagents...")
    import smolagents
    print(f"smolagents version: {smolagents.__version__}")
    
    print("\nImporting tools...")
    from tools import get_current_weather, simple_calculator
    print("Tools imported successfully")
    
    print("\nChecking tool attributes...")
    print(f"get_current_weather.__module__: {get_current_weather.__module__}")
    print(f"simple_calculator.__module__: {simple_calculator.__module__}")
    
    print("\nTest completed successfully")
except Exception as e:
    print(f"Error: {e}")
