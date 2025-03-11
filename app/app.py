
from flask import Flask, render_template, request, session, redirect, url_for
import requests as req
import json
from argparse import ArgumentParser

from routes.items import item_bp
from routes.categories import cat_bp
from routes.dashboard import dash_bp
from routes.api.user import User
from flask_login import current_user, LoginManager

app = Flask(__name__)
app.secret_key = "secret"
app.config["API_BASE_URL"] = "http://127.0.0.1:8080"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):
    response = req.post(f"{app.config["API_BASE_URL"] }/user/{user_id}").json()
    if response["response"] == 200:
        data = response["data"]
        print(f"User created with email {data["email"]}")
        return User(user_id=data["id"],
                    firstname=data["firstname"],
                    lastname=data["lastname"],
                    email=data["email"],
                    is_admin=data["is_admin"])
    return None

from routes.auth import auth_bp

app.register_blueprint(auth_bp)
app.register_blueprint(dash_bp)
app.register_blueprint(cat_bp)
app.register_blueprint(item_bp)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(503)
def service_unavailable(error):
    return render_template('api_error.html'), 503


if __name__ == '__main__':
    app.run()

