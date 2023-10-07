#!/usr/bin/env python3
import argparse
import logging
import os
import re
import socket
from getpass import getuser

import webcolors
from i3ipc import Connection

from i3_ssh_title_updater.constants import (
    ALLOWED_WARN_TEXT_PATTERN,
    DEFAULT_FONT_COLOR,
    DEFAULT_WARN_TEXT,
)
from i3_ssh_title_updater.helpers import (
    FontColorValidationError,
    WarnTextValidationError,
    is_valid_html_color,
    validate_font_color,
    validate_warn_text,
)


def parse_command_line_arguments() -> argparse.Namespace:
    """
    Parse the command line arguments and return the parsed arguments.

    This function uses the argparse module to define and parse command line arguments.
    It creates an ArgumentParser object and adds various arguments to it,
    including the following:

    - `--connect`: A boolean flag that indicates whether to use the connection option 
        before connecting to an SSH server.
    - `--disconnect`: A boolean flag that indicates whether to use the disconnection
        option after connecting to an SSH server.
    - `--font_color`: A string that specifies the foreground HTML color to use for the
        window title. The default value is `DEFAULT_FONT_COLOR`.
    - `--warn_text`: A string that specifies a custom warning text to display for
        production servers. The default value is `DEFAULT_WARN_TEXT`.

    The function then parses the command line arguments using the `parse_args()` method
    of the ArgumentParser object.
    It checks if the provided `font_color` is a valid HTML color code or a known
    color name and raises a `ValueError`
    if it is not. It also validates the `warn_text` using the defined pattern and raises
    a `ValueError` if it contains
    invalid characters.

    If a valid color name is provided for `font_color`, the function converts it
    to an HTML color code
    using the `name_to_hex()` function from the `webcolors` module.

    Returns:
        An `argparse.Namespace` object that contains the parsed command line arguments.

    Raises:
        ValueError: If the provided `font_color` is not a valid HTML color code or color
        name, or if the `warn_text` contains invalid characters.
    """
    parser = argparse.ArgumentParser(
        description='Automatically update the i3wm window' +
        ' title when connecting to an SSH server')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--connect", action='store_true', help='Use before SSH connection'
    )
    group.add_argument(
        "--disconnect", action='store_true', help='Use after SSH connection'
    )
    parser.add_argument(
        '--font_color', action='store', dest='font_color', metavar='color',
                        help='Foreground HTML color (e.g., "#bf616a" or red)',
                        default=DEFAULT_FONT_COLOR)
    parser.add_argument('--warn_text', action='store', dest='warn_text',
                        help='Custom warning text for production servers',
                        default=DEFAULT_WARN_TEXT)

    args = parser.parse_args()

    # Check if the provided font_color is a valid HTML color code or a known color name
    if not is_valid_html_color(args.font_color):
        raise ValueError(
        'Invalid font color format. Please use a valid HTML color code or color name.')

    # Validate the warn_text using the defined pattern
    if args.warn_text and not re.match(ALLOWED_WARN_TEXT_PATTERN, args.warn_text):
        raise ValueError(
        'Invalid characters in warn_text.'+
        ' Please use only alphanumeric characters and allowed symbols.')

    # Convert color name to HTML color code if a valid color name is provided
    if not args.font_color.startswith('#'):
        args.font_color = webcolors.name_to_hex(args.font_color)

    return args


class WindowTitleUpdater:
    """
    A class for updating the i3wm window title based on SSH connections.

    This class provides methods to set the window title with custom formatting
    depending on whether an SSH connection is established or disconnected.

    Args:
        args (argparse.Namespace): Command-line arguments and configurations.

    Attributes:
        args (argparse.Namespace): The parsed command-line arguments.
        i3_connection (i3ipc.Connection): The connection to the i3 window manager.
        focused_window (i3ipc.Con)nection): The currently focused window.

    Methods:
        set_window_title(title: str):
            Sets the window title to the provided title.

        get_remote_title() -> str:
            Generates a formatted title for a remote SSH connection.

        get_local_title() -> str:
            Generates a formatted title for the local shell.

        format_local_title(user: str, hostname: str, current_directory: str) -> str:
            Formats a local shell title with user, hostname, and current directory.
    """

    def __init__(self, args):
        self.args = args
        self.i3_connection = None
        self.focused_window = None
        try:
            self.i3_connection = Connection()
            self.focused_window = self.i3_connection.get_tree().find_focused()
        except Exception as e:
            logging.error('Could not establish an IPC connection to i3: %s', str(e))
            exit(1)

    def set_window_title(self, title: str):
        """
        Set the window title for the focused window.

        Args:
            title (str): The new title to be set for the window.

        Note:
            This method updates the title of the currently focused window

        Example:
            To set the window title to 'My Window', use:
            ```
            title_updater.set_window_title('My Window')
            ```
        """
        self.focused_window.command(f'title_format {title}')

    def get_remote_title(self) -> str:
        """
        Get the remote title for the window.

        Returns:
            str: The remote title in a formatted string with font color and warning text
        """
        span_start = f'<span size="x-large" foreground="{self.args.font_color}">'
        warning_text = f' {self.args.warn_text}'
        server_name = self.focused_window.name.replace('ssh ', '')
        return f'{span_start}{warning_text} {server_name}</span>'

    def get_local_title(self) -> str:
        """
        Get the local title for the window.

        Returns:
            str: The local title in the format 'user@hostname: current_directory'.
        """
        user = getuser()
        hostname = socket.gethostname()
        current_directory = os.getcwd().replace(os.path.expanduser("~"), "~")
        return self.format_local_title(user, hostname, current_directory)

    def format_local_title(
        self, user: str, hostname: str, current_directory: str) -> str:
        """
        Format the local title for the window.

        Args:
            user (str): The current user's username.
            hostname (str): The hostname of the local machine.
            current_directory (str): The current working directory.

        Returns:
            str: The formatted local title 
                in the format 'user@hostname: current_directory'.
        """
        return '{}@{}: {}'.format(user, hostname, current_directory)


def main():
    """
    Execute the main logic of the program.

    This function is responsible for executing the main logic of the program.
        It performs the following steps:
    1. Parse the command line arguments using the 
        `parse_command_line_arguments()` function.
    2. Validate the font color specified in the command line arguments 
        using the `validate_font_color()` function.
    3. Validate the warning text specified in the command line 
        arguments using the `validate_warn_text()` function.
    4. Create an instance of the `WindowTitleUpdater` 
        class with the command line arguments.
    5. If the `connect` flag is set to `True` in the command line arguments
        , set the window title to the remote title using the `set_window_title()`
            and `get_remote_title()` methods of the `WindowTitleUpdater` class.
    6. If the `disconnect` flag is set to `True` in the command line arguments
        , set the window title to the local title using the `set_window_title()`
        and `get_local_title()` methods of the `WindowTitleUpdater` class.

    Raises:
        FontColorValidationError: If the validation of the font color fails.
        WarnTextValidationError: If the validation of the warning text fails.
        Exception: If an unexpected error occurs.

    Returns:
        None
    """
    try:
        args = parse_command_line_arguments()
        validate_font_color(args.font_color)
        validate_warn_text(args.warn_text)

        title_updater = WindowTitleUpdater(args)
        if args.connect:
            title_updater.set_window_title(title_updater.get_remote_title())
        elif args.disconnect:
            title_updater.set_window_title(title_updater.get_local_title())
    except FontColorValidationError as e:
        logging.error('Font color validation error: %s', str(e))
        exit(1)
    except WarnTextValidationError as e:
        logging.error('Warn text validation error: %s', str(e))
        exit(1)
    except Exception as e:
        logging.error('An unexpected error occurred: %s', str(e))
        exit(1)


if __name__ == "__main__":
    """
    Main entry point of the script.

    This function is responsible for parsing command-line arguments
        , validating input values,
    and updating the i3 window manager window title based on the provided arguments.

    It handles exceptions and logs errors in case of validation or unexpected errors.

    Usage:
        This function is automatically called when the script is executed.

    Example:
        To run the script:
        ```
        if __name__ == "__main__":
            main()
        ```
    """
    main()
