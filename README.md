# Gitbot

![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)

This is a Git agent on the local network, running on Discord and Slack.

![Example](featured.png)

## Installation

It's a very small package, so you can easily install, update and delete it.

```bash
python -m pip install -U -e git+ssh://git@github.com/oshinko/bot.git@next#egg=bot-0.0.0
python -m pip install -U -e git+ssh://git@github.com/oshinko/gitbot.git@draft#egg=gitbot-0.0.0
```

## Startup

```bash
python -m bot --space bot.spaces.Discord \
              --token ${BOT_TOKEN} \
              --modules gitbot.std \
              --errorsto "#errors"
```

## Commands

See the [real code](gitbot/std.py).

### Hello

Return information including SSH key.

```bash
hello
```

### Init

Create an empty Git repository.

```bash
init <repo>
```

### Publish

リポジトリをリモートリポジトリに転送します。

```bash
publish <namespace>/<local-repo> <remote-repo>
```

### Subscribe

リモートリポジトリをリポジトリに紐付けます。

その後、購読という形で定期的に同期 (fetch) されます。

```bash
subscribe <remote-repo> <local-repo>
```
