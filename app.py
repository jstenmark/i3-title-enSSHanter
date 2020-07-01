#!/usr/bin/env python3
from i3ipc import Connection, Event

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

        if sys.argv[1] == 'disconnect':
            title = '{}@{}:{}'.format(
                    getuser(),
                    gethostname(),
                    getcwd().replace(path.expanduser("~"), "~"))
            self.set_title(title)
        elif sys.argv[1] == 'connect':
            title = self.ctx.name.replace("ssh ", "")
            self.set_title(f'<span  size="x-large" foreground="#bf616a">   PRODUCTION SERVER:  { title }  </span>')

if __name__ == "__main__":
    Checker().check()
