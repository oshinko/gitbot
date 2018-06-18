from asyncio import create_subprocess_exec, subprocess
from base64 import b64decode, b64encode
from bot import hear, task
from datetime import timedelta
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


def encode(s):
    return b64encode(s.encode()).decode().rstrip('=')


@hear('[Ss]ubscribe (.+) to (.+)', channels=channels, ambient=True)
async def subscribe(message, remote, local):
    remote_name = encode(remote)
    local_repo = repo_path(local)
    if local_repo.is_dir():
        c = ['git', 'remote', 'add', remote_name, remote]
        p = await create_subprocess_exec(*c,
                                         cwd=local_repo,
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE)
        outs, errs = await p.communicate()
    else:
        c = ['git', 'clone', remote, str(local_repo), '--origin', remote_name,
             '--progress']
        p = await create_subprocess_exec(*c,
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE)
        outs, errs = await p.communicate()
    reply = (outs or errs).decode() or f'Subscribed {remote} to {local}.'
    await message.reply(reply)


@task(timedelta(hours=1))
async def fetch():
    for repo in Path.home().iterdir():
        if repo.suffix == '.git':
            c = ['git', 'remote', '-v']
            p = await create_subprocess_exec(*c,
                                             cwd=repo,
                                             stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE)
            outs, _ = await p.communicate()
            if outs:
                c = ['git', 'fetch', '--all', '--progress']
                p = await create_subprocess_exec(*c,
                                                 cwd=repo,
                                                 stdout=subprocess.PIPE,
                                                 stderr=subprocess.PIPE)
                await p.communicate()
