from flask import Blueprint, url_for, request, flash, render_template
from flask_login import login_required, logout_user, login_user
from werkzeug.utils import redirect
from .api import auth_requests
from .api.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print("Log in form")
        email = request.form["email"]
        password = request.form["password"]

        status, data = auth_requests.login_user(email, password)

        print(status)

        if status == 200:
            user = User(data["id"],
                        data["firstname"],
                        data["lastname"],
                        data["email"],
                        data["is_admin"])

            login_user(user)
            return redirect(url_for("dashboard.dashboard"))
        else:
            flash("Invalid email or password", "danger")

    return render_template("login.html")

@auth_bp.route('/auth/create', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_p = request.form["confirm_password"]

        if password != confirm_p:
            flash("Passwords do not match.", "danger")
            return redirect(url_for("auth.register"))

        if email == "admin@wholehealth.com":
            is_admin = True
        else:
            is_admin = False

        status, data = auth_requests.new_user(firstname, lastname, email, password, is_admin)

        if status == 200:
            print("200 CREATED")
            flash("Account created successfully!", "success")
            return redirect(url_for("auth.login"))
        elif status == 400:
            print("400 NOT CREATED")
            flash("This email is already in use.", "Danger")
            return redirect(url_for("auth.register"))
        else:
            print("500 NOT CREATED")
            flash("Internal Server Error occurred, please try again later.", "danger")
            return redirect(url_for("auth.register"))

    return render_template("register.html")


@auth_bp.route('/auth/logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for("dashboard.dashboard"))