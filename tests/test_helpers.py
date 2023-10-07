import unittest

from i3_ssh_title_updater.helpers import (
    FontColorValidationError,
    is_valid_html_color,
    validate_font_color,
    validate_warn_text,
)


class TestFontColorValidation(unittest.TestCase):

    def test_valid_color(self):
        # Test a valid HTML color code
        color = '#ff0000'
        result = is_valid_html_color(color)
        self.assertTrue(result)

    def test_valid_color_name(self):
        # Test a valid HTML color name
        color = 'red'
        result = is_valid_html_color(color)
        self.assertTrue(result)

    def test_invalid_color(self):
        # Test an invalid color
        color = 'invalid_color'
        result = is_valid_html_color(color)
        self.assertFalse(result)

    def test_valid_font_color(self):
        # Test valid font color
        color = '#00ff00'
        validate_font_color(color)  # This should not raise an exception

    def test_invalid_font_color(self):
        # Test invalid font color
        color = 'invalid_color'
        with self.assertRaises(FontColorValidationError):
            validate_font_color(color)

class TestWarnTextValidation(unittest.TestCase):

    def test_valid_warn_text(self):
        # Test valid warn text
        text = 'Warning: This is a test!'
        validate_warn_text(text)


if __name__ == '__main__':
    unittest.main()
