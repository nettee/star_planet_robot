import getpass
from fabric import task, Connection, Config

host = 'william@106.14.207.119'

tar_file = 'star_planet_robot.tar.gz'
target_dir = '/home/william/star_planet_robot/'
service_name = 'star_planet_robot'


@task
def pack(c):
    conn = Connection(host)
    conn.local('mkdir -p ./dist/')
    conn.local('rm -f ./dist/{}'.format(tar_file))
    # Pack executable files
    includes = ['*.py']
    excludes = ['fabfile.py', 'test.py', '.*', '*.pyc']
    cmd = ['tar', '-czvf', './dist/{}'.format(tar_file)]
    cmd.extend('--exclude="{}"'.format(ex) for ex in excludes)
    cmd.extend(includes)
    conn.local(' '.join(cmd))


@task
def upload(c):
    conn = Connection(host)
    result = conn.put('./dist/{}'.format(tar_file), remote='/tmp/')
    print('Uploaded {0.local} to {0.remote}'.format(result))


@task
def unpack(c):
    conn = Connection(host)
    conn.run('mkdir -p {}'.format(target_dir))
    conn.run('tar -C {} -xzvf /tmp/{}'.format(target_dir, tar_file))


@task
def deploy(c):
    pack(c)
    upload(c)
    unpack(c)


@task
def restart_server(c):
    password = getpass.getpass('Your sudo password: ')
    config = Config(overrides={'sudo': {'password': password}})
    conn = Connection(host, config=config)
    commands = [
        'supervisorctl stop {}'.format(service_name),
        'supervisorctl start {}'.format(service_name),
        '/etc/init.d/nginx reload',
    ]
    for cmd in commands:
        conn.sudo(cmd, hide='stderr')


