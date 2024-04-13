from invoke import task

@task
def setup(c):
    c.run("pip install -r requirements.txt")

@task
def dev(c):
    c.run("flask --app app run")