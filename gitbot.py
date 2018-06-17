from asyncio import create_subprocess_exec, subprocess
from bot import hear, task
from datetime import time
from pathlib import Path

channels = ['#test']


@hear('[Hh]ello', channels=channels, ambient=True)
async def hello(message):
    with (Path.home() / '.ssh/id_rsa.pub').open() as f:
        await message.reply(f"""Hi! It's a My SSH key.
{f.readline()}""")


def repo_path(repo):
    p = Path.home() / repo
    if p.suffix != '.git':
        p = p.with_suffix('.git')
    return p


@hear('[Ii]nit (.+)', channels=channels, ambient=True)
async def init(message, repo):
    c = ['git', 'init', '--bare', str(repo_path(repo))]
    p = await create_subprocess_exec(*c,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
    outs, errs = await p.communicate()
    await message.reply((outs or errs).decode())


@hear('[Pp]ublish (.+) as (.+) to (.+)', channels=channels, ambient=True)
async def publish(message, local, name, remote):
    d = repo_path(local)
    c = ['git', 'show-ref', '--heads', '--tags']
    p = await create_subprocess_exec(*c,
                                     cwd=d,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
    outs, errs = await p.communicate()
    if outs:
        reply = ''
        for line in outs.decode().splitlines():
            h, r = line.split(' ')
            ref = Path(r)
            prefix = ref.parts[:2]
            suffix = ref.parts[2:]
            remote_ref = Path(*prefix + (name,) + suffix)
            c = ['git', 'push', remote, f'{r}:{remote_ref}']
            p = await create_subprocess_exec(*c,
                                             cwd=d,
                                             stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE)
            outs, errs = await p.communicate()
            reply += f"""**{r} to {remote_ref}**
{(outs or errs).decode().strip()}

"""
        await message.reply(f"""Published {d.absolute()} as {name} to {remote}.

{reply.strip()}""")
    elif errs:
        await message.reply(errs.decode())
    else:
        await message.reply(('Publish was canceled because '
                             'reference was not found in the repository.'))


@hear('[Ss]ubscribe (.+) to (.+)', channels=channels, ambient=True)
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
    # for ref in Path.home().iterdir():
    #     pass
