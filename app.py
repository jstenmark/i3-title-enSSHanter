#!/usr/bin/env python3
from i3ipc import Connection

import sys
from os import getcwd, path
from socket import gethostname
from getpass import getuser


class Checker():
    ctx = None

    def __init__(self):
        try:
            self.ctx = Connection().get_tree().find_focused()
        except Exception as e:
            print('Could not connect to i3 ipc')
            print(e)

    def set_title(self, title):
        self.ctx.command(f'title_format { title }')

    def check(self):
        if len(sys.argv) <= 1:
            print('No args found. Please use "connect" or "disconnect"')
            exit(1)

        if sys.argv[1] == 'connect':
            start = '<span  size="x-large" foreground="#bf616a">'
            warn_text = '  PRODUCTION SERVER:'
            title_text = self.ctx.name.replace('ssh ', '')
            end = ' </span>'
            self.set_title(f'{ start }{ warn_text } { title_text } { end }')
        elif sys.argv[1] == 'disconnect':
            title = '{}@{}:{}'.format(
                    getuser(),
                    gethostname(),
                    getcwd().replace(path.expanduser("~"), "~"))
            self.set_title(title)


if __name__ == "__main__":
    Checker().check()
