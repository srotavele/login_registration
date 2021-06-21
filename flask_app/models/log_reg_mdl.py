from ..config.mysqlconnections import connectToMySQL
from flask import flash
import re


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.birthdate = data['email']
        self.password = data['password']
        self.password_confirm = data['password_confirm']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
        
    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM users;'
        results = connectToMySQL('login_registration_schema').query_db(query)
        clients = []
        
        for row in results:
            clients.append(User(row))
        return clients


    @staticmethod
    def validate_registration(post_data):
        is_valid = True
        if len(post_data['first_name']) < 2:
            flash("First name must be at least two characters.")
            is_valid = False
            
        if len(post_data['last_name']) < 2:
            flash("Last Name must be at least two characters.")
            is_valid = False
            
        if len(post_data['birthdate']) < 2:
            flash("You must be at least 10 years old to register.")
            is_valid =  False
            
        if len(post_data['password']) < 1:
            flash("Yo.")
            is_valid = False
            
        return is_valid

    @staticmethod
    def validate_email(post_data):
        is_valid = True
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):
            flash("Email is not valid.")
            is_valid = False
            
        return is_valid