from invoke import task


@task
def setup(c):
    c.run("pip install -r requirements.txt")


@task
def dev(c):
    c.run("python wsgi.py")

@task
def migrate(c):
    c.run("flask db upgrade")
