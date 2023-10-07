import re

import webcolors

from i3_ssh_title_updater.constants import ALLOWED_WARN_TEXT_PATTERN


class FontColorValidationError(Exception):
    """
    Exception raised for invalid font color.

    Attributes:
        message (str): Explanation of the error.
    """
    pass


class WarnTextValidationError(Exception):
    """
    Exception raised for invalid warning text.

    Attributes:
        message (str): Explanation of the error.
    """
    pass

def validate_font_color(color: str):
    """
    Validates the font color by checking if it is a valid HTML color code or color name.

    Parameters:
        color (str): The font color to be validated.

    Raises:
        FontColorValidationError: If the font color is not a valid HTML color code or color name.
    """
    if not is_valid_html_color(color):
        raise FontColorValidationError('Invalid font color format. Please use a valid HTML color code or color name.')

def validate_warn_text(text: str):
    """
    Validate the warn text format.

    Args:
        text (str): The warn text to validate.

    Raises:
        WarnTextValidationError: If the warn text contains invalid characters.
    """
    if text and not re.match(ALLOWED_WARN_TEXT_PATTERN, text):
        raise WarnTextValidationError('Invalid characters in warn_text. Please use only alphanumeric characters and allowed symbols.')


def is_valid_html_color(color: str) -> bool:
    """
    Check if a color is a valid HTML color code or name.

    Args:
        color (str): The color to check.

    Returns:
        bool: True if the color is valid, False otherwise.
    """
    # Check if the color is a valid HTML color code (e.g., "#RRGGBB" or "#RRGGBBAA")
    if re.match(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{8})$', color):
        return True

    # Use webcolors library to validate HTML color names
    try:
        webcolors.name_to_hex(color)
        return True
    except ValueError:
        return False
