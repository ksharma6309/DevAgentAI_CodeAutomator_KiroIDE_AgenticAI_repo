"""Simple math utilities for demo."""

def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def divide(a, b):
    if b == 0:
        raise ValueError("Division by zero")
    return a / b
