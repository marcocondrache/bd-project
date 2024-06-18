import os

from invoke import task
from sqlalchemy import create_engine

from config import Dev
from factory.populate import Populate


def generate(c):
    c.run("npx tailwindcss -i ./app/static/src/input.css -o ./app/static/dist/css/output.css --minify")


@task
def populate(c):
    migrate(c)

    c.run('echo "This might take a while since a lot of data is created..."')

    engine = create_engine(Dev.SQLALCHEMY_DATABASE_URI)
    populator = Populate(engine.connect())

    populator.populate()
    engine.dispose()


@task
def setup(c):
    # Install deps
    c.run("pip install -r requirements.txt")
    c.run("npm install")
    c.run("npx tailwindcss -i ./app/static/src/input.css -o ./app/static/dist/css/output.css --minify")

    # Generate secret and other env variables
    env = open('.env', 'w+')
    env.write("SECRET_KEY={secret}".format(secret=os.urandom(32)))


@task
def dev(c):
    os.environ.update({'FLASK_CONFIG_DEFAULT': 'Dev'})
    c.run("npx tailwindcss -i ./app/static/src/input.css -o ./app/static/dist/css/output.css --minify")
    c.run("python wsgi.py")


@task
def migrate(c):
    c.run("flask db upgrade")
