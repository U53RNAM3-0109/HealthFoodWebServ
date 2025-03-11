from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user_id, firstname, lastname, email, is_admin):
        self.id = user_id
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.is_admin = is_admin