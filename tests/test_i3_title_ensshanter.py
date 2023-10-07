import argparse
import unittest
from unittest.mock import MagicMock, patch

from i3_ssh_title_updater.i3_title_ensshanter import WindowTitleUpdater


class TestWindowTitleUpdater(unittest.TestCase):
    def setUp(self):
        self.args = argparse.Namespace(
            connect=True,
            disconnect=False,
            font_color="#ff0000",
            warn_text="SSH Server"
        )
        self.args.user = "test_user"
        self.args.hostname = "test_hostname"
        self.args.current_directory = "/home/test_user"
        self.title_updater = WindowTitleUpdater(self.args)
        self.title_updater.focused_window = MagicMock()
        self.title_updater.focused_window.name.replace.return_value = "ssh ExampleServer"

    def test_set_window_title(self):
        self.title_updater.set_window_title("Test Title")
        self.title_updater.focused_window.command.assert_called_once_with('title_format Test Title')

    def test_get_remote_title(self):
        self.args.font_color = "#ff0000"
        self.args.warn_text = "SSH Server"
        expected_title = '<span size="x-large" foreground="#ff0000"> SSH Server ssh ExampleServer</span>'
        title = self.title_updater.get_remote_title()
        self.assertEqual(title, expected_title)

    @patch('i3_ssh_title_updater.i3_title_ensshanter.getuser', return_value='test_user')
    @patch('socket.gethostname', return_value='test_hostname')
    @patch('os.getcwd', return_value='/home/test_user')
    def test_get_local_title(self, mock_getuser, mock_gethostname, mock_getcwd):
        expected_title = 'test_user@test_hostname: /home/test_user'
        title = self.title_updater.get_local_title()
        self.assertEqual(title, expected_title)

    def test_format_local_title(self):
        user = "test_user"
        hostname = "test_hostname"
        current_directory = "/home/test_user"
        expected_title = f'{user}@{hostname}: {current_directory}'
        title = self.title_updater.format_local_title(user, hostname, current_directory)
        self.assertEqual(title, expected_title)


if __name__ == '__main__':
    unittest.main()
