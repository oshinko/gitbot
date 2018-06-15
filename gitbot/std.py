from bot import hear
from pathlib import Path

channels = ['#test']


@hear('[Ii]nit (.+)', channels=channels, ambient=True)
async def init(message, repo):
    # mkdir $HOME/repo
    # cd $HOME/repo
    # git init --bare
    r = Path.home().joinpath(repo)
    await message.reply(f'Initialized empty Git repository in {r}')


@hear('[Pp]ush (.+) (.+) (.+)', channels=channels, ambient=True)
async def push(message, local, remote, refspec):
    # cd $HOME/local
    # git push remote refspec
    await message.reply(f'Pushed {local} to {remote}')


@hear('[Pp]ull (.+) (.+) (.+)', channels=channels, ambient=True)
async def pull(message, local, remote, refspec):
    # cd $HOME/local
    # git fetch remote refspec
    await message.reply(f'Pulled {remote} to {local}')
