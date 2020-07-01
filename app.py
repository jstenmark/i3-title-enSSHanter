#!/usr/bin/env python3
from i3ipc import Connection

import sys
from os import getcwd, path
from socket import gethostname
from getpass import getuser

args_error = 'Invalid args. Please use "connect" or "disconnect"'
font_color = '#bf616a'


class Checker():
    def __init__(self):
        try:
            self.ctx = Connection().get_tree().find_focused()
        except Exception as e:
            print('Could not connect to i3 ipc')
            exit(e)

    def check(self):
        if sys.argv[1] == 'connect':
            self.set_title(self.get_warn_format())
        elif sys.argv[1] == 'disconnect':
            title = '{}@{}: {}'.format(
                    getuser(),
                    gethostname(),
                    getcwd().replace(path.expanduser("~"), "~"))
            self.set_title(title)
        else:
            exit(args_error)

    def set_title(self, title):
        self.ctx.command(f'title_format { title }')

    def get_warn_format(self):
        span_start = f'<span  size="x-large" foreground="{ font_color }">'
        warn_text = '   PRODUCTION SERVER:'
        title_text = self.ctx.name.replace('ssh ', '')
        return f'{ span_start }{ warn_text } { title_text } </span>'


if __name__ == "__main__":
    if len(sys.argv) == 2:
        Checker().check()
    else:
        exit(args_error)
