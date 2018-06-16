from bot import hear, task
from datetime import time
from pathlib import Path

channels = ['#test']


@hear('[Hh]ello', channels=channels, ambient=True)
async def hello(message):
    await message.reply(f'Hi! My SSH key is XXXX.')


@hear('[Ii]nit (.+)', channels=channels, ambient=True)
async def init(message, repo):
    # mkdir $HOME/repo
    # cd $HOME/repo
    # git init --bare
    r = Path.home().joinpath(repo)
    await message.reply(f'Initialized empty Git repository in {r}.')


@hear('[Pp]ublish (.+)[/ ](.+) (.+)', channels=channels, ambient=True)
async def publish(message, namespace, local, remote):
    # cd $HOME/local
    # # for REF in $LOCAL_REFS:
    #   git push remote $REF:namespace/$REF
    await message.reply(f'Published {namespace}/{local} to {remote}.')


@hear('[Ss]ubscribe (.+) (.+)', channels=channels, ambient=True)
async def subscribe(message, remote, local):
    # REMOTE=`echo -n remote | base64 | sed -e 's/=*$//'`
    # if [ -d $HOME/local ]; then
    #   cd $HOME/local
    #   git remote add $REMOTE local
    # else
    #   git clone remote $HOME/local --origin $REMOTE
    # fi
    await message.reply(f'Subscribed {remote} to {local}.')


@task(time(hour=0))
async def fetch():
    # for repo in $HOME:
    #   cd repo
    #   git fetch --all
    pass
