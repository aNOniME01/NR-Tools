def adjust_text_number(text: str, adjustment: int, prefix: str = "") -> str:
    """
    Adjusts the numeric part of a string by a specified amount.

    Args:
        text (str): The input string (e.g., "uv_2").
        adjustment (int): The amount to adjust (positive to increment, negative to decrement).
        prefix (str): An optional prefix to match and preserve (e.g., "uv_").

    Returns:
        str: The adjusted string (e.g., "uv_3").
    """
    number = 0

    # Check if the text starts with the given prefix
    if text.startswith(prefix):
        try:
            # Extract the numeric part of the string
            number = int(text[len(prefix):])
        except ValueError:
            pass  # If no number is present, default to 0

    # Adjust the numeric value and clamp it at 0
    number = max(0, number + adjustment)

    # Return the adjusted string
    return f"{prefix}{number}"
