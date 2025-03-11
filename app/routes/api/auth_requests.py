import json
from flask import current_app, render_template
import requests

def new_user(firstname, lastname, email, password, is_admin=False):
    url = f"{current_app.config["API_BASE_URL"]}/user"

    body = {
        "firstname":firstname,
        "lastname":lastname,
        "email":email,
        "password":password,
        "is_admin":is_admin
    }

    try:
        response = requests.post(url, json=body).json()
    except requests.exceptions.ConnectionError:
        # Handle specific connection error (e.g., when the API is down)
        return render_template('api_error.html'), 503
    except requests.exceptions.RequestException as e:
        # Catch other types of request exceptions (timeouts, etc.)
        print(f"Request Error: {e}")
        return render_template('api_error.html'), 503


    if response["response"] == 200:
        return 200, response["data"]
    elif response["response"] == 400:
        return 400, None
    else:
        return 500, None

def login_user(email, password):
    url = f"{current_app.config["API_BASE_URL"]}/auth"

    body = {
        "email":email,
        "password":password
    }

    try:
       response = requests.post(url, json=body).json()
    except requests.exceptions.ConnectionError:
        # Handle specific connection error (e.g., when the API is down)
        return render_template('api_error.html'), 503
    except requests.exceptions.RequestException as e:
        # Catch other types of request exceptions (timeouts, etc.)
        print(f"Request Error: {e}")
        return render_template('api_error.html'), 503

    if response["response"] == 200:
        url = f"{current_app.config["API_BASE_URL"]}/user/{response["data"]['id']}"

        try:
            response = requests.post(url).json()
        except requests.exceptions.ConnectionError:
            # Handle specific connection error (e.g., when the API is down)
            return render_template('api_error.html'), 503
        except requests.exceptions.RequestException as e:
            # Catch other types of request exceptions (timeouts, etc.)
            print(f"Request Error: {e}")
            return render_template('api_error.html'), 503

        if response["response"] == 200:
            return 200, response["data"]
        else:
            return 400, None
    elif response["response"] == 401:
        return 401, None
    else:
        return 500, None
