from asyncio import create_subprocess_exec, subprocess
from base64 import b64decode, b64encode
from bot import hear, task
from datetime import timedelta
from os import environ
from pathlib import Path

try:
    channels = environ['GITBOT_CHANNELS'].split(' ')
except KeyError:
    channels = []
else:
    channels = [x for x in channels if x]


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


async def run(*args, cwd=None):
    return await create_subprocess_exec(*args,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        cwd=cwd)


@hear('[Ii]nit (.+)', channels=channels, ambient=True)
async def init(message, repo):
    p = await run('git', 'init', '--bare', str(repo_path(repo)))
    outs, errs = await p.communicate()
    await message.reply((outs or errs).decode())


@hear('[Pp]ublish (.+) as (.+) to (.+)', channels=channels, ambient=True)
async def publish(message, local, name, remote):
    local_repo = repo_path(local)
    p = await run('git', 'show-ref', '--heads', '--tags', cwd=local_repo)
    outs, errs = await p.communicate()
    if outs:
        reply = ''
        for line in outs.decode().splitlines():
            h, r = line.split(' ')
            ref = Path(r)
            prefix = ref.parts[:2]
            suffix = ref.parts[2:]
            remote_ref = Path(*prefix + (name,) + suffix)
            p = await run('git', 'push', remote, f'{r}:{remote_ref}',
                          cwd=local_repo)
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


def encode(s):
    return b64encode(s.encode()).decode().rstrip('=')


@hear('[Ss]ubscribe (.+) to (.+)', channels=channels, ambient=True)
async def subscribe(message, remote, local):
    remote_name = encode(remote)
    local_repo = repo_path(local)
    if local_repo.is_dir():
        p = await run('git', 'remote', 'add', remote_name, remote,
                      cwd=local_repo)
        outs, errs = await p.communicate()
    else:
        p = await run('git', 'clone', remote, str(local_repo),
                      '--origin', remote_name, '--progress')
        outs, errs = await p.communicate()
    reply = (outs or errs).decode() or f'Subscribed {remote} to {local}.'
    await message.reply(reply)


@task(timedelta(hours=1))
async def fetch():
    for repo in Path.home().iterdir():
        if repo.suffix == '.git':
            p = await run('git', 'remote', '-v', cwd=repo)
            outs, _ = await p.communicate()
            if outs:
                p = await run('git', 'fetch', '--all', '--progress', cwd=repo)
                await p.communicate()
