import base64

import requests
from flask import Blueprint, url_for, request, flash, render_template, current_app
from flask_login import login_required, current_user
from werkzeug.utils import redirect

cat_bp = Blueprint('category', __name__)

@cat_bp.route('/category/')
def cat_def():
    return redirect(url_for('dashboard.dashboard'))

# Route to display items for a specific category
@cat_bp.route('/category/<category_name>', methods=['GET'])
def category_items(category_name):
    url = f"{current_app.config["API_BASE_URL"]}/category/{category_name}?detailed=True"

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
        return render_template('category.html', category_data = data)
    else:
        return redirect(url_for('dashboard.dashboard'))


@cat_bp.route('/new/category', methods=['GET','POST'])
@login_required
def category_submit():
    if current_user.is_admin:
        if request.method == 'POST':
            url = f"{current_app.config["API_BASE_URL"]}/category"

            title = request.form.get('title')
            url_ext = request.form.get('url_ext')
            image_f = request.files.get('image')
            snippet = request.form.get('snippet')
            description = request.form.get('description')

            img_type = image_f.content_type
            image = base64.b64encode(image_f.read()).decode()

            body = {
                'title':title,
                'snippet':snippet,
                'description':description,
                'url_ext':url_ext,
                'image_64':image,
                'image_format':img_type
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
                return redirect(url_for('category.category_items', category_name=url_ext))
            else:
                flash("Invalid submission", 'danger')
                return redirect(url_for('category.category_submit'))
        else:
            return render_template('new_category.html')
    else:
        return redirect(url_for('dashboard.dashboard'))

@cat_bp.route('/delete/category/<category_name>', methods=['POST'])
def delete_category(category_name):
    if current_user.is_admin:
        url = f"{current_app.config["API_BASE_URL"]}/category/{category_name}"

        try:
            response = requests.delete(url).json()

        except requests.exceptions.ConnectionError:
            # Handle specific connection error (e.g., when the API is down)
            return render_template('api_error.html'), 503
        except requests.exceptions.RequestException as e:
            # Catch other types of request exceptions (timeouts, etc.)
            print(f"Request Error: {e}")
            return render_template('api_error.html'), 503

        if response["response"] == 200:
            flash("Category removed.", "success")
            return redirect(url_for('dashboard.dashboard'))

        else:
            flash("Deletion failed.", "warning")
            return redirect(url_for('category.category_items', category_name=category_name))

    flash("You do not have permission to perform this action.", "warning")
    return redirect(url_for('category.category_items', category_name=category_name))


@cat_bp.route('/update/category/<category_name>', methods=['GET', 'POST'])
def update_category(category_name):
    if request.method == 'GET':
        url_ext = category_name

        url = f"{current_app.config["API_BASE_URL"]}/category/{category_name}?detailed=True"

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
            return render_template('update_category.html', category=data)
        else:
            flash("Category does not exist.")
            return redirect(url_for('dashboard.dashboard'))

    if request.method == 'POST':

        url = f"{current_app.config["API_BASE_URL"]}/category/{category_name}?detailed=True"

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

            title = request.form.get('title', None)
            url_ext = request.form.get('url_ext', None)
            image_f = request.files.get('image_f', None)
            snippet = request.form.get('snippet', None)
            description = request.form.get('description', None)

            if image_f:
                image_format = image_f.content_type
                image = base64.b64encode(image_f.read()).decode()
                print("new image")
            else:
                image_format = None
                image = None

            category_data = {
                'title': title if title else data['title'],
                'url_ext': url_ext if url_ext else data['url_ext'],
                'image_f': image if image else data['image_64'],
                'image_format': image_format if image_format else data['image_format'],
                'snippet': snippet if snippet else data['snippet'],
                'description': description if description else data['description'],
            }

            print(snippet)

            url = f"{current_app.config['API_BASE_URL']}/category/{data['url_ext']}"

            try:
                response = requests.patch(url, json=category_data).json()
            except requests.exceptions.ConnectionError:
                # Handle specific connection error (e.g., when the API is down)
                return render_template('api_error.html'), 503
            except requests.exceptions.RequestException as e:
                # Catch other types of request exceptions (timeouts, etc.)
                print(f"Request Error: {e}")
                return render_template('api_error.html'), 503


            if response['response'] == 200:
                flash("Updated successfully.", 'success')
                return redirect(url_for('category.category_items', category_name=category_name))

            else:
                flash("Update unsuccessful.", 'warning')

        else:
            flash("Category does not exist.")
            return redirect(url_for('dashboard.dashboard'))

