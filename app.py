#!/usr/bin/env python3
from i3ipc import Connection

import argparse
import sys

from os import getcwd, path
from socket import gethostname
from getpass import getuser

parser = argparse.ArgumentParser(
    description='Change i3 window title when ssh to a prod server.')
group = parser.add_mutually_exclusive_group()
group.add_argument("--connect",
                   action='store_true',
                   help='Use before ssh connection')
group.add_argument("--disconnect",
                   action='store_true',
                   help='Use after ssh connection')
parser.add_argument('--font_color',
                    action='store',
                    dest='font_color',
                    help='foreground color code. eg: #bf616a or red',
                    default='#bf616a')
args = parser.parse_args()


class Checker():
    def __init__(self):
        try:
            self.ctx = Connection().get_tree().find_focused()
        except Exception as e:
            print('Could not connect to i3 ipc')
            exit(e)

    def check(self):
        if args.connect:
            self.set_title(self.get_warn_title())

        if args.disconnect:
            title = '{}@{}: {}'.format(
                    getuser(),
                    gethostname(),
                    getcwd().replace(path.expanduser("~"), "~"))
            self.set_title(title)

    def set_title(self, title):
        self.ctx.command(f'title_format { title }')

    def get_warn_title(self):
        span_start = f'<span  size="x-large" foreground="{ args.font_color }">'
        warn_text = '   PRODUCTION SERVER:'
        title_text = self.ctx.name.replace('ssh ', '')
        return f'{ span_start }{ warn_text } { title_text } </span>'


if __name__ == "__main__":
    if len(sys.argv) < 2:
        parser.print_usage()
        sys.exit(1)
    else:
        Checker().check()
