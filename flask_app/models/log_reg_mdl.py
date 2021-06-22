from ..config.mysqlconnections import connectToMySQL
from flask import flash
import re
from flask_app import app
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.birthdate = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def get_all(cls):
        pass
    
    
    @classmethod
    def create(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, birthdate, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(birthdate)s, %(password)s, NOW(), NOW());"
        
        results = connectToMySQL('login_registration_schema').query_db(query, data)
        return results


    @classmethod
    def get_by_email(cls,data):
        query = 'SELECT * FROM users WHERE email = %(email)s;'

        results = connectToMySQL('login_registration_schema').query_db(query, data)
        if len(results) < 1:
            return False
        return User(results[0])


    @classmethod
    def get_by_id(cls,data):
        query = 'SELECT * FROM users WHERE id = %(id)s;'

        results = connectToMySQL('login_registration_schema').query_db(query, data)
        return User(results[0])


    @classmethod
    def update_edit():
        pass


    @staticmethod
    def validate_signup (post_data):
        is_valid = True
        if len(post_data['first_name']) < 2:
            flash("First Name must be at least two characters.")
            is_valid = False

        if len(post_data['last_name']) < 2:
            flash("Last Name must be at least two characters.")
            is_valid = False

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):
            flash("Email is not valid.")
            is_valid = False

        if len(post_data['birthdate']) < 2:
            flash("You must be at least 10 years old to register.")
            is_valid =  False

        if len(post_data['password']) < 4:
            flash("Password must longer.")
            is_valid = False
        PASSWORD_REGEX = re.compile('\d.*[A-Z]|[A-Z].*\d')
        if not PASSWORD_REGEX.match(post_data['password']):
            flash('Password must contain ONE capital letter and ONE number.')
        else:
            if post_data['password'] != post_data['confirm_password']:
                flash('Passwords do not match.')
                is_valid = False

        return is_valid


    @staticmethod
    def validate_login (post_data):
        user_from_db = User.get_by_email({'email': post_data['email']})
        if not user_from_db:
            flash('invalid credentials')
            return False
        if not bcrypt.check_password_hash(user_from_db.password,post_data['password']):
            flash('Invalid Credentials.')
            return False
        
        return True