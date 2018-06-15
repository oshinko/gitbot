# Gitbot

![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)

This is a Git agent on the local network, running on Discord and Slack.

![Example](featured.png)

## Commands

See the [real code](gitbot/std.py).

### Init

```bash
init <repo>
```

### Push

```bash
push <local-repo> <remote-repo> <refspec>
```

### Pull

```bash
pull <local-repo> <remote-repo> <refspec>
```

## Installation

It's a very small package, so you can easily install, update and delete it.

```bash
python -m pip install -U -e git+ssh://git@github.com/oshinko/bot.git@next#egg=bot-0.0.0
python -m pip install -U -e git+ssh://git@github.com/oshinko/gitbot.git@next#egg=gitbot-0.0.0
```

## Startup

```bash
python -m bot --space bot.spaces.Discord \
              --token ${BOT_TOKEN} \
              --modules gitbot.std \
              --errorsto "#errors"
```
