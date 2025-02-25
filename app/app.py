
from flask import Flask, render_template, request
import requests as req
import json

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('login_signup.html')

API_HOST = "http://52.156.24.253"  # Replace with your actual API hostname


@app.route('/user', methods=['POST'])
def create_user():
    # Get data from the request
    data = request.json
    # Send data to the API
    response = req.post(f"{API_HOST}/user", json=data)

    data = json.loads(response)

    if data["response"] == 200:
        return "User created!"
    else:
        return "Failed to make user!"


@app.route('/auth', methods=['POST'])
def login_user():
    # Get login data from request
    data = request.json
    # Send login request to the API
    response = req.post(f"{API_HOST}/auth", json=data)

    if data["response"] == 200:
        return "Successful login"
    else:
        return "Failed login"


if __name__ == '__main__':
    app.run(debug=True)

app.run(debug=True)