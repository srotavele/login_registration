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
    