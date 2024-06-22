import os

from invoke import task
from sqlalchemy import create_engine

from config import Dev
from factory.populate import Populate


def generate_styles(c):
    s = f"npx tailwindcss -i ./app/static/*.css -o ./app/static/dist/output.css --minify"
    c.run(s)
    print("styles generated")


def generate_secret():
    secret_entry = "SECRET_KEY="
    env_path = ".env"

    if not os.path.exists(env_path):  # .env file does not exist, create it
        with open(env_path, "w") as env_file:
            env_file.write(f"{secret_entry}{os.urandom(32)}\n")
            print(f"generated .env file with secret key")
    else:
        with open(env_path, "r") as env_file:
            lines = env_file.readlines()

        for line in lines:  # check if secret key already exists
            if line.startswith(secret_entry):
                print("secret key already exists in .env file, skipping...")
                return

        with open(env_path, "a") as env_file:  # append secret key to .env file
            env_file.write(f"{secret_entry}{os.urandom(32)}\n")
            print("appended secret key to .env file")


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
    generate_secret()


@task
def dev(c):
    generate_styles(c)
    os.environ.update({'FLASK_CONFIG_DEFAULT': 'Dev'})
    c.run("python wsgi.py")


@task
def migrate(c):
    c.run("flask db upgrade")
