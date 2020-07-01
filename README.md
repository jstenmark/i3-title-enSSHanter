# Change i3 window title depending on ssh connection

Verified working with i3+termite.

Does not work when reusing a ssh session with the ssh `ControlMaster` setting


## Requirements

Needs i3wm, python3, and ssh

## Usage

1. Add the ssh alias to your aliases file and reload your shell
2. Add the app to you bin path, eg:

```bash
ln -s ~/i3-ssh-autotitle/app.py ~/.local/bin/check-ssh-status
```
Or skip symlink and use absolute path in your ssh config

3. Add the ssh config
