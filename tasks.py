import os

from invoke import task
from sqlalchemy import create_engine

from config import Dev
from factory.populate import Populate


def generate_styles(c):
    s = f"npx tailwindcss -i ./app/static/*.css -o ./app/static/dist/output.css --minify"
    c.run(s)
    print("styles generated")


@task
def populate(c):
    migrate(c)

    print("This might take a while since a lot of data is created...")

    engine = create_engine(Dev.SQLALCHEMY_DATABASE_URI)
    populator = Populate(engine.connect())

    populator.populate()
    engine.dispose()


@task
def setup(c):
    # Install deps
    c.run("pip install -r requirements.txt")
    c.run("npm install")

    generate_styles(c)

    # Generate secret and other env variables
    env = open('.env', 'w+')
    env.write("SECRET_KEY={secret}".format(secret=os.urandom(32)))


@task
def dev(c):
    generate_styles(c)
    os.environ.update({'FLASK_CONFIG_DEFAULT': 'Dev'})
    c.run("python wsgi.py")


@task
def migrate(c):
    c.run("flask db upgrade")
