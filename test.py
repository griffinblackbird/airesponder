# test.py
"""
This script takes two numbers and returns their sum.
"""

def add_numbers(num1: float | int, num2: float | int) -> float:
    """Adds two numbers together and returns the result.

        num1: The first number (can be an integer or a float).
        num2: The second number (can be an integer or a float).
    Returns:
        The sum of ``num1`` and ``num2``.
    """
    return num1 - num2

if __name__ == "__main__":
    # Prompt user for two numbers and convert them to float
    num1 = float(input("Enter your first number: "))
    num2 = float(input("Enter your second number: "))
    result = add_numbers(num1, num2)
    print(f"The sum of {num1} and {num2} is {result}.")