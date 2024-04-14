from invoke import task

@task
def setup(c):
    c.run("pip install -r requirements.txt")

@task
def dev(c):
    c.prefix("FLASK_CONFIG_DEFAULT=Dev")
    c.run("python wsgi.py")