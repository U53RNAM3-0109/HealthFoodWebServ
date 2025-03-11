import base64
from requests.exceptions import ConnectionError
import requests
from flask import Blueprint, url_for, request, flash, render_template, current_app
from flask_login import login_required, logout_user, login_user, current_user
from werkzeug.utils import redirect
from .api import auth_requests
from .api.user import User

dash_bp = Blueprint('dashboard', __name__)

@dash_bp.route('/', methods=['GET'])
def dashboard():
    url = f"{current_app.config["API_BASE_URL"]}/category?detailed=True"
    try:
        response = requests.get(url).json()

    except requests.exceptions.ConnectionError:
        # Handle specific connection error (e.g., when the API is down)
        return render_template('api_error.html'), 503
    except requests.exceptions.RequestException as e:
        # Catch other types of request exceptions (timeouts, etc.)
        print(f"Request Error: {e}")
        return render_template('api_error.html'), 503

    if response["response"] == 200:
        data = response["data"]
        return render_template('index.html', category_data = data)
    else:
        return render_template('index.html')