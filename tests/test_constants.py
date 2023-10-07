import unittest

from i3_ssh_title_updater.constants import ALLOWED_WARN_TEXT_PATTERN


class TestAllowedWarnTextPattern(unittest.TestCase):
    def test_valid_patterns(self):
        valid_patterns = [
            'ValidText',
            '1234567890',
            '!@#$%^&*()-_=+[]{};:"<>,.?/\\',
        ]

        for pattern in valid_patterns:
            with self.subTest(pattern=pattern):
                self.assertRegex(pattern, ALLOWED_WARN_TEXT_PATTERN)

    def test_valid_max_length(self):
        valid_max_length_patterns = [
            'A' * 100,  # Exactly 100 characters
            'B' * 50 + 'C' * 50,  # Total 100 characters
        ]

        for pattern in valid_max_length_patterns:
            with self.subTest(pattern=pattern):
                self.assertRegex(pattern, ALLOWED_WARN_TEXT_PATTERN)

    def test_invalid_patterns(self):
        invalid_patterns = [
            'This is too long' * 1,  # Exceeds 100 characters
            'Text with spaces',
            'Text_with_underscore',
        ]

        for pattern in invalid_patterns:
            with self.subTest(pattern=pattern):
                self.assertRegex(pattern, ALLOWED_WARN_TEXT_PATTERN)


if __name__ == '__main__':
    unittest.main()
