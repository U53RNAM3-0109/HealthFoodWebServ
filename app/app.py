
from flask import Flask, render_template, request
import requests as req
import json
from argparse import ArgumentParser

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('login_signup.html', resp="")

API_HOST = "http://52.156.24.253"  # Replace with your actual API hostname


@app.route('/user', methods=['POST'])
def create_user():
    # Get data from the request
    parser = ArgumentParser
    parser.add_argument("email", type=str)
    parser.add_argument("password", type=str)
    parser.add_argument("firstname", type=str)
    parser.add_argument("lastname", type=str)
    parser.add_argument("usertype", type=str)

    data = parser.parse_args()

    print(data['firstname'])

    # Send data to the API
    response = req.post(f"{API_HOST}/user", json=data)

    data = json.loads(response)

    if data["response"] == 200:
        return render_template("login_signup.html", resp="User created!")
    else:
        return render_template("login_signup.html", resp=f"User not created!\nMessage:{data['message']}")


@app.route('/auth', methods=['POST'])
def login_user():
    # Get login data from request
    data = request.json
    # Send login request to the API
    response = req.post(f"{API_HOST}/auth", json=data)

    data = json.loads(response)

    if data["response"] == 200:
        return render_template("login_signup.html", resp=f"Logged in! User:{data['data']['id']}")
    else:
        return render_template("login_signup.html", resp=f"User not logged in\nMessage:{data['message']}")


if __name__ == '__main__':
    app.run(debug=True)

app.run(debug=True)