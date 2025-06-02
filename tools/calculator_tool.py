from typing import Dict, Any, Literal
from smolagents import tool

@tool
def simple_calculator(operand1: float, operand2: float, operation: str) -> float:
    """
    Perform basic arithmetic operations: add, subtract, multiply, divide.
    
    Args:
        operand1 (float): First number for the operation
        operand2 (float): Second number for the operation
        operation (str): Operation to perform (add/subtract/multiply/divide)
        
    Returns:
        float: The result of the arithmetic operation
        
    Raises:
        ValueError: If division by zero is attempted or invalid operation
    """
    print(f"Calculating {operand1} {operation} {operand2}")
    
    if operation == 'add':
        return float(operand1 + operand2)
    elif operation == 'subtract':
        return float(operand1 - operand2)
    elif operation == 'multiply':
        return float(operand1 * operand2)
    elif operation == 'divide':
        if operand2 == 0:
            raise ValueError("Cannot divide by zero")
        return float(operand1 / operand2)
    else:
        raise ValueError(f"Invalid operation: {operation}")

# For backward compatibility
SimpleCalculatorTool = simple_calculator
