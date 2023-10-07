# i3-title-enSSHanter
**Automagically Enhance i3 Window Manager Title When Summoning SSH Connections like a Wizard, especially to Production Servers, with a side of graphical pizzazz!**

## Table of Contents

- [i3-title-enSSHanter](#i3-title-enSSHanter)
  - [Introduction](#introduction)
    - [The Scientific Pursuit Behind i3-title-enSSHanter](#the-scientific-pursuit-behind-i3-title-enSSHanter)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Options](#options)
  - [Limitations](#limitations)
    - [ControlMaster Setting](#controlmaster-setting)
    - [LocalCommand Setting](#localcommand-setting)
    - [SSH Configurations](#ssh-configurations)
    - [Network Latency](#network-latency)
    - [Workarounds](#workarounds)
      - [Using a Wrapper Script](#using-a-wrapper-script)
      - [Using Tmux or Screen](#using-tmux-or-screen)
      - [Using the PROMPT_COMMAND Environment Variable](#using-the-prompt_command-environment-variable)
  - [Contact](#contact)
  - [Contributing](#contributing)
  - [License](#license)

## Introduction
Have you ever accidentally run critical commands on the wrong server? The `i3-title-enSSHanter` script is a meticulously crafted utility designed to automatically modify the current window terminal title when establishing SSH connections, possibly to production servers, providing a graphical alert. This graphical alert mechanism provides an immediate visual cue, reinforcing a heightened awareness of the operational context.

`i3-title-enSSHanter` seamlessly integrates into existing workflows, effectively alerting users to their environment without disrupting i3's visual harmony.

### The Scientific Pursuit Behind i3-title-enSSHanter
The fervent desire to optimize terminal workflows was born from the trenches of network operations. It was there, amidst the tangle of cables and humming server rooms, that the spark for this ingenious script was kindled.

In this quest for terminal transcendence, the creator of `i3-title-enSSHanter` delved deep into the realms of i3 ricing. The objective was clear: to mitigate the risk of inadvertently executing detrimental commands within an intricate server ecosystem.

>*And then there was that unforgettable incident, a tale we couldn't resist sharing. You see, a colleague from a distinguished establishment once embarked on an unexpected 'rm -rf' journey into the prod database data folder. The potential disaster loomed large, but swift action and exemplary sysadmin skills averted the impending catastrophe.*

Why such a passion for terminal perfection? Well, it's a saga rooted in the noblest of pursuits - the relentless quest for that elusive blend of productivity and whimsy that only sysadmins, network operators, and such creatures truly understand.

### Disclaimer
Hey there, fellow explorer of the grand realm of tiling window managers! We want to make it crystal clear that we harbor no trace of elitism here. You are absolutely free to choose any window manager that tickles your fancy, and we promise not to raise an eyebrow or cast judgment on your life choices. After all, the aesthetics of a terminal are as unique as the fingerprints on your favorite coffee mug.

We wholeheartedly support your unalienable right to create your own GUI/TUI utopia, and we even sprinkle a bit of fairy dust on it for good measure. 😄

So, whether you're a seasoned Arch ricer or a curious newcomer, we're here to make your terminal adventures a tad more enchanting. Happy hacking! 🚀

>*If you're curious about the creator's "avoidant attachment style" with [Sway](https://swaywm.org/), well, let's just say it's a story that may or may not involve a lot of tabbed containers.*

## Prerequisites
Before you get started, ensure you have the following prerequisites:

- Python 3.x
- deep [ssh_config](https://man.openbsd.org/ssh_config) knowledge (optional)
- [i3-title-enSSHanter](https://github.com/jstenmark/i3-title-enSSHanter)
- [i3wm](https://i3wm.org/)
- [i3ipc-python](https://github.com/altdesktop/i3ipc-python)

## Installation
Getting started with `i3-title-enSSHanter` is easy. Follow these steps to set it up:



1. **Install Dependencies:**

   - Make sure you have the required dependencies installed.

   ```bash
   pip install -r requirements.txt
   ```

2. **Add the script to your `PATH`:**
   >To make it easily accessible, you can add the script to a directory included in your `PATH`, (e.g., your `bin` folder).
     ```bash
     # With a symbolic link
     ln -s ~/i3-title-enSSHanter/app.py ~/.local/bin/i3-title-enSSHanter
     ```

     Alternatively, if you prefer not to use a symbolic link, you can skip this step and use an absolute path in `LocalCommand` later.

3. **Create an SSH Wrapper Alias:**
   >To integrate `i3-title-enSSHanter` seamlessly, you can create an SSH wrapper alias. Add the following lines to your shell's profile (e.g., ~/.bashrc or ~/.zshrc) , and don't forget to reload your shell:
   ```bash
   #!/bin/bash
   ssh() {
      command ssh "$@"

      # After the SSH connection, run 'i3-title-enSSHanter' with the '--disconnect' flag
      # to reset the window title to its default state.
      i3-title-enSSHanter --disconnect
   }
   ```

4. **Configure Your SSH Config:**
   >Edit your `~/.ssh/config` file to specify which hosts should trigger `i3-title-enSSHanter`. For example:
   ```ssh-config
   Host *prod* !*dev* examplehost1* examplehost2.com
       PermitLocalCommand yes
       LocalCommand i3-title-enSSHanter --connect
   ```
   This configuration ensures that `i3-title-enSSHanter` is activated when you connect to specific hosts that match the provided patterns.

## Usage
Using `i3-title-enSSHanter` is as delightful as a rainbow after a rainstorm (well, almost). Once you've set it up as described in the installation instructions, here's how you can use it:

- Simply SSH into one of your production servers using your preferred terminal.
- As soon as you establish the SSH connection, you'll witness a burst of colors in your terminal window title, something like this:

   ```bash
   🌈  WELCOME TO THE LAND OF SERVERS! 🦄
   ```

- And remember, when you're done with your magical server adventure, the title will transform again:

   ```bash
   🪄  BACK TO REALITY: Your desk misses you! 🌟
   ```

   Your desktop environment beckons, and your desk eagerly awaits your return, but don't forget to bring some of that server magic with you!


### Options
**--warn_text**
>Modify the warning text

```bash
i3-title-enSSHanter --warn_text "⚠️  DANGER ZONE: Do not touch anything! ⚠️"
```

**--font_color**
>Set title text color
```bash
i3-title-enSSHanter --connect --font_color red   --warn_text "Danger! Beware of dragons (or bugs)!"
i3-title-enSSHanter --connect --font_color blue  --warn_text "A calm and tranquil server for serene coding sessions."
i3-title-enSSHanter --connect --font_color green --warn_text "Safe and sound, the server is your playground."
```


**--disconnect**
>You can also reset the title if youre experiencing any issues when you're done with your work.

```bash
i3-title-enSSHanter --disconnect
```

## Limitations
<details>
  <summary>ControlMaster Setting</summary>

  SSH's `ControlMaster` setting, when used in SSH configurations, may interfere with the terminal title change mechanism. When `ControlMaster` is active, SSH multiplexes connections, which means that new connections may not reset the terminal title as expected. Users who rely heavily on `ControlMaster` should be aware that the terminal title may not always reflect the active SSH session. Manpage [ssh_config#ControlMaster](https://man.openbsd.org/ssh_config#ControlMaster).
</details>
<details>
  <summary>LocalCommand Setting</summary>

  Ah, the majestic `LocalCommand` option in SSH, the chosen one among a sea of mundane alternatives. Why bother with those ordinary, straightforward solutions when you can wield the power of `LocalCommand`? It's the ultimate way to add complexity to your life.

   You see, why settle for a simple Bash function or a wrapper script when you can embrace the mystique of `LocalCommand`? It's like the dark arts of SSH configuration. Sure, it might seem a bit cryptic at first, but that's the charm of it, right?

   Why take the easy road of creating a custom script when you can indulge in the enigma of SSH's local execution command? It's like solving a riddle every time you connect to a server. Will it work this time, or will it unleash unexpected surprises? Who knows?

   So, if you're a true connoisseur of SSH configuration, forget simplicity and embrace the challenge. Use `LocalCommand` and let the adventure begin. Who needs straightforward solutions when you can have SSH configurations that keep you guessing at every turn?
</details>
<details>
  <summary>SSH Configurations</summary>

  `i3-title-enSSHanter` relies on SSH configurations to trigger automatic title changes. If your SSH configurations are not set up correctly or do not match the specified patterns, the title change may not occur as expected. Double-check your SSH configurations to ensure they align with your intended usage.
</details>
<details>
  <summary>Network Latency</summary>

  In cases of high network latency or slow SSH connection establishment, the title change may not be immediate. There could be a slight delay between establishing the connection and the title update.
</details>

### Workarounds
To achieve the behavior of modifying the terminal title when connecting to an SSH server without using the `LocalCommand` option in your SSH configuration, you have a few alternatives:

<details>
  <summary>Using a Wrapper Script</summary>

   Ah, the classic wrapper script - the knight in shining armor of the terminal world. Create your custom script, bestow it with the +x permission, and let it escort you through the SSH

   ```bash
   #!/bin/bash
   ssh "$@"
   echo -ne "\033]0;Your Title Here\007" # Replace "Your Title Here" with your desired enchanting title.
   ```

   Make sure to give execute permission to the script using `chmod +x myssh`.
</details>
<details>
  <summary>Using Tmux or Screen</summary>

   If you use terminal multiplexers like Tmux or Screen, you can set the terminal title using their respective commands when creating or attaching to sessions. This approach provides more flexibility if you're already using these tools.
</details>
<details>
  <summary>Using the PROMPT_COMMAND-Environment Variable</summary>

   You can set the `PROMPT_COMMAND` environment variable in your shell's profile file to run a command before each prompt. Inside this command, you can check if you're in an SSH session and set the terminal title accordingly.

   ```bash
   PROMPT_COMMAND='if [[ -n "$SSH_CLIENT" ]]; then echo -ne "\033]0;Your Title Here\007"; fi'
   ```

   This approach automatically updates the title whenever you open an SSH connection.
</details>


<details>
  <summary>Click to expand/collapse</summary>

  This is the content that can be expanded or collapsed.
</details>

## Contact
If you encounter any issues or have questions, feel free to contact mapmaker of this digital treasure hunt!

- [GitHub](https://github.com/jstenmark)
- [GitHub issues](https://github.com/jstenmark/i3-title-enSSHanter/issues)
- [LinkedIn](https://www.linkedin.com/in/johannes-stenmark-57a290a7/)

## Contributing
Ahoy, brave soul! So, you've decided to embark on a perilous journey into the depths of our codebase? Well, we must commend your adventurous spirit! 🏴‍☠️

Contributing to the `i3-title-enSSHanter` project is like discovering hidden treasure in a vast sea of code. However, we must warn you that our treasure chest may contain a few surprises - think mischievous code gremlins and pixelated pirates. But fret not, for every contribution, no matter how small or swashbuckling, is truly appreciated.

If you're ready to set sail, please consult our [contributing guide](127.0.0.1:5000/docs/contributing). Although, we must confess, we don't really expect anyone to contribute. It's not like this project is worth anyone's time, right? Yet, should you choose to join our merry band of code adventurers, prepare for a voyage filled with unexpected twists and, perhaps, a barrel of virtual grog. 🍻

Arrr! The code be open source, and the winds be in your favor. ⛵


## License
This project is licensed under the [MIT License](LICENSE.md).

Feel free to do whatever you want with it. We won't be bothered, and neither will the code gremlins. They're a resilient bunch!

🪄✨