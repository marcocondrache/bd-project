import os

from invoke import task


@task
def setup(c):
    # Install deps
    c.run("pip install -r requirements.txt")

    # Generate secret and other env variables
    env = open('.env', 'w+')
    env.write("SECRET_KEY={secret}".format(secret=os.urandom(32)))


@task
def dev(c):
    os.environ.update({'FLASK_CONFIG_DEFAULT': 'Dev'})
    c.run("python wsgi.py")


@task
def migrate(c):
    c.run("flask db upgrade")
