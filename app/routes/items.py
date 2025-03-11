import base64
import requests
from flask import Blueprint, url_for, request, flash, render_template, current_app
from flask_login import login_required, current_user
from werkzeug.utils import redirect
import re

item_bp = Blueprint('item', __name__)

# Route to display items for a specific category
@item_bp.route('/item/<item_id>', methods=['GET'])
def item_details(item_id):
    url = f"{current_app.config["API_BASE_URL"]}/item/{item_id}?detailed=True"

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
        return render_template('item.html', item_data=data)
    else:
        return redirect(url_for('dashboard.dashboard'))

@item_bp.route('/new/item', methods=['GET', 'POST'])
@login_required
def item_submit():
    if current_user.is_admin:
        if request.method == 'POST':
            url = f"{current_app.config['API_BASE_URL']}/item"

            title = request.form.get('title')
            snippet = request.form.get('snippet')
            description = request.form.get('description')
            price = request.form.get('price')
            category_id = request.form.get('category_id')
            image_f = request.files.get('image')

            img_type = image_f.content_type
            image = base64.b64encode(image_f.read()).decode()

            body = {
                'title': title,
                'snippet': snippet,
                'description': description,
                'price': price,
                'category_id': category_id,
                'image_64': image,
                'image_format': img_type
            }

            if not validate_price(price):
                flash("Price is invalid.", 'warning')
                return redirect(url_for('item.item_submit'))

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
                return redirect(url_for('category.category_items', category_name=response["data"]["cat_url_ext"]))
            else:
                flash("Invalid submission", 'danger')
                return redirect(url_for('item.item_submit'))
        else:
            # Fetch categories for the dropdown
            url = f"{current_app.config['API_BASE_URL']}/category"

            try:
                response = requests.get(url).json()
            except requests.exceptions.ConnectionError:
                # Handle specific connection error (e.g., when the API is down)
                return render_template('api_error.html'), 503
            except requests.exceptions.RequestException as e:
                # Catch other types of request exceptions (timeouts, etc.)
                print(f"Request Error: {e}")
                return render_template('api_error.html'), 503

            categories = response.get('data', [])

            return render_template('new_item.html', categories=categories)
    else:
        return redirect(url_for('dashboard.dashboard'))


@item_bp.route('/delete/item/<item_id>')
def delete_item(item_id):
    if current_user.is_admin:
        url = f"{current_app.config["API_BASE_URL"]}/item/{item_id}"

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
            flash("Item removed.", "success")
            return redirect(url_for('dashboard.dashboard'))

        else:
            flash("Deletion failed.", "warning")
            return redirect(url_for('item.item_details', item_id=item_id))

    flash("You do not have permission to perform this action.", "warning")
    return redirect(url_for('item.item_details', item_id=item_id))

@item_bp.route('/update/item/<item_id>', methods=['GET', 'POST'])
def update_item(item_id):
    if request.method == 'GET':
        url = f"{current_app.config["API_BASE_URL"]}/item/{item_id}?detailed=True"

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
            return render_template('update_item.html', item=data)
        else:
            flash("Item does not exist.")
            return redirect(url_for('dashboard.dashboard'))

    if request.method == 'POST':
        url = f"{current_app.config["API_BASE_URL"]}/item/{item_id}?detailed=True"

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
            snippet = request.form.get('snippet', None)
            description = request.form.get('description', None)
            price = request.form.get('price', None)
            category_id = request.form.get('category_id', None)
            image_f = request.files.get('image_f', None)

            if image_f:
                image_format = image_f.content_type
                image = base64.b64encode(image_f.read()).decode()
            else:
                image_format = None
                image = None

            item_data = {
                'title': title if title else data['title'],
                'snippet': snippet if snippet else data['snippet'],
                'description': description if description else data['description'],
                'price': price if price else data['price'],
                'category_id': category_id if category_id else data['category_id'],
                'image_64': image if image else data['image_64'],
                'image_format': image_format if image_format else data['image_format'],
            }

            url = f"{current_app.config['API_BASE_URL']}/item/{data['id']}"

            try:
                response = requests.patch(url, json=item_data).json()
            except requests.exceptions.ConnectionError:
                # Handle specific connection error (e.g., when the API is down)
                return render_template('api_error.html'), 503
            except requests.exceptions.RequestException as e:
                # Catch other types of request exceptions (timeouts, etc.)
                print(f"Request Error: {e}")
                return render_template('api_error.html'), 503

            if response['response'] == 200:
                flash("Updated successfully.", 'success')
                return redirect(url_for('item.item_details', item_id=item_id))

            else:
                flash("Update unsuccessful.", 'warning')

        else:
            flash("Item does not exist.")
            return redirect(url_for('dashboard.dashboard'))



def validate_price(price):
    # Check if the price matches the GBP format (e.g., 10.99)
    if not re.match(r'^\d+(\.\d{1,2})?$', price):
        return False
    return True

