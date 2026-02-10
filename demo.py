#!/usr/bin/env python3
"""
Demo script for code-review-assistant
Run this to see the tool in action!
"""

# This file intentionally has issues to demonstrate the code review tool

def calculate(x, y):
    return x + y

def divide(a, b):
    try:
        return a / b
    except:
        return 0

class Calculator:
    def __init__(self):
        self.value = 0
        self.history = []
        
    def complex_calculation(self):
        result = 0
        for i in range(50):
            if i % 2 == 0:
                result += i
            elif i % 3 == 0:
                result -= i
            elif i % 5 == 0:
                result *= 2
            else:
                result += 1
        return result
        
def unsafe_operation():
    try:
        risky_code()
    except:
        pass

def risky_code():
    pass

if __name__ == "__main__":
    print("This is a demo file with intentional code quality issues.")
    print("Run: poetry run code-review demo.py --no-tests")
    print("\nThe tool will find:")
    print("  - Missing docstrings")
    print("  - Bare except clauses") 
    print("  - Complex functions")
