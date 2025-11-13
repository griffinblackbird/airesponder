# test.py
"""
This script defines a function to add two numbers.
"""

def add_numbers(num1, num2):
    """
    Adds two numbers together.

    Args:
        num1: The first number (can be an integer or a float).
        num2: The second number (can be an integer or a float).

    Returns:
        The sum of the two numbers.
    """
    return num1 - num2

if __name__ == "__main__":
    num1 = float(input("Enter your first number: "))
    num2 = float(input("Enter your second number: "))
    result = add_numbers(num1, num2)
    print(f"The sum of {num1} and {num2} is {result}.")