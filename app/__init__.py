
from flask import Flask, render_template, request, session, redirect, url_for
import requests as req
import json
from argparse import ArgumentParser

from .routes.items import item_bp
from .routes.categories import cat_bp
from .routes.dashboard import dash_bp
from .routes.api.user import User
from .routes.auth import auth_bp
from flask_login import current_user, LoginManager

class WholeHealthWebServ(Flask):

    def __init__(self, __name__, api_url):
        super().__init__(__name__, template_folder='app/templates', static_folder='app/static')
        self.secret_key = "secret"
        self.config["API_BASE_URL"] = api_url

        login_manager = LoginManager()
        login_manager.init_app(self)
        login_manager.login_view = "auth.login"

        @login_manager.user_loader
        def load_user(user_id):
            response = req.post(f"{self.config["API_BASE_URL"] }/user/{user_id}").json()
            if response["response"] == 200:
                data = response["data"]
                print(f"User created with email {data["email"]}")
                return User(user_id=data["id"],
                            firstname=data["firstname"],
                            lastname=data["lastname"],
                            email=data["email"],
                            is_admin=data["is_admin"])
            return None



        self.register_blueprint(auth_bp)
        self.register_blueprint(dash_bp)
        self.register_blueprint(cat_bp)
        self.register_blueprint(item_bp)

        @self.errorhandler(404)
        def page_not_found(error):
            return render_template('404.html'), 404

        @self.errorhandler(503)
        def service_unavailable(error):
            return render_template('api_error.html'), 503

