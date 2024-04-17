from app.modules.auth import auth


@auth.route("/login")
def login():
    return "test"
