# i3-ssh-autotitle

**Change i3 window title when ssh to a prod server**

When SSH'ing to a prod server, `LocalCommand` will run this script which changes the terminal title to something more alerting, intending to stop you from running commands in the wrong terminal window.

A shell alias wraps `ssh` to trigger the scrip again when the session is disconnected, thus resetting the terminal title.

The ssh `LocalCommand` is supposed to match on production servers, otherwise the ssh alias wrapper could initiate this app.


## Requirements

`i3`, `python3`

Verified with termite.

## Installation
- Install dependencies `install -r requirements.txt`

- Add the app to you bin path
	- `ln -s ~/i3-ssh-autotitle/app.py ~/.local/bin/check-ssh-status`

	- Or skip the symlink and use an absolute path in `LocalCommand`

- Add the ssh alias to your aliases file and reload your shell (eg `~/.bashrc`).

- Add config from `ssh_config` to your `~/.ssh/config`, add prod servers as you like.

## Usage

SSH to one of your prod servers and watch your terminal title change.

Note: The `LocalCommand` setting does not get executed when reusing a ssh socket with `ControlMaster`.
