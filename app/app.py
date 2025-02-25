
from flask import Flask, render_template, request, session
import requests as req
import json
from argparse import ArgumentParser

app = Flask(__name__)

app.secret_key = "THISISASECRETKEY"

@app.route("/")
def index():
    return render_template('login_signup.html', resp="")

API_HOST = "http://52.156.24.253"  # Replace with your actual API hostname

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', default=None)

    return render_template('login_signup.html', resp="")

@app.route('/user', methods=['POST'])
def create_user():
    # Get data from the request

    data = {
        "email": request.form.get("email"),
        "password": request.form.get("password"),
        "firstname": request.form.get("firstname"),
        "lastname": request.form.get("lastname"),
        "usertype": request.form.get("usertype")
    }

    # Send data to the API
    response = req.post(f"{API_HOST}/user", json=data)

    data = response.json()

    if data["response"] == 200:
        return render_template("login_signup.html", resp="User created!")
    else:
        return render_template("login_signup.html", resp=f"User not created!\nMessage:{data['message']}")


@app.route('/auth', methods=['POST'])
def login_user():
    # Get login data from request
    data = {
        "email": request.form.get("email"),
        "password": request.form.get("password")
    }

    # Send login request to the API
    response = req.post(f"{API_HOST}/auth", json=data)

    data = response.json()


    if data["response"] == 200:

        session["user_id"] = data["data"]["id"]
        return render_template("login_signup.html", resp=f"Logged in! User:{data['data']['id']}")
    else:
        return render_template("login_signup.html", resp=f"User not logged in\nMessage:{data['message']}")


if __name__ == '__main__':
    app.run(debug=True)

app.run(debug=True)