from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.__init__ import DATABASE
from flask import flash
from flask_bcrypt import Bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__( self , data ): 
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipe_items = []


# # CLASS METHODS # #

#Login and Reg
    @classmethod
    def save(cls, form_data):
        query = '''
            INSERT INTO users (first_name, last_name, email, password)
            VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)
        '''
        user_id = connectToMySQL(DATABASE).query_db(query, form_data)
        return user_id
    
    @classmethod
    def get_by_email(cls, email):
        email_dict = {'email' : email}
        query = '''
            SELECT * FROM users
            WHERE email = %(email)s;
        '''

        results = connectToMySQL(DATABASE).query_db(query, email_dict)

        if len(results) < 1:
            return False
        found_user = cls(results[0])
        return found_user
    
    @classmethod
    def get_one_by_id(cls, id):
        id_dict = {'id' : id}
        query = '''
            SELECT * FROM users
            WHERE id = %(id)s;
        '''
        results = connectToMySQL(DATABASE).query_db(query, id_dict)
        user = cls(results[0])
        return user
    

#CRUD

    # READ ALL
    @classmethod
    def get_all(cls):
        query = '''
            SELECT * FROM users;
        '''
        results = connectToMySQL(DATABASE).query_db(query)

        users = []

        for row in results:
            new_user = cls(row)
            users.append(new_user)

        return users


    #READ ONE
    @classmethod
    def get_one(cls, id):
        data = {'id': id}
        query = '''
            SELECT * FROM users WHERE id = %(id)s;
        '''
        result = connectToMySQL(DATABASE).query_db(query, data)
        return User(result[0])


    #UPDATE
    @classmethod
    def update(cls, data):
        query = '''
            UPDATE users 
            SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s
            WHERE id = %(id)s;
        '''
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results


    #DELETE
    @classmethod
    def delete(cls, id):
        data = {'id': id}
        query = '''
        DELETE FROM users WHERE id = %(id)s;
        '''
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result



# # STATIC METHODS # #

    @staticmethod
    def validate_user(data):
        is_valid = True

        if len(data['first_name']) < 3:
            flash('First name must be at least 3 characters', 'register')
            is_valid = False

        if len(data['last_name']) < 3:
            flash('Last name must be at least 3 characters', 'register')
            is_valid = False

        if len(data['email']) < 3:
            flash('Email must be at least 3 characters', 'register')
            is_valid = False

        if len(data['password']) < 8:
            flash('Password must be at least 8 characters', 'register')
            is_valid = False

        if len(data['confirm_pw']) < 8:
            flash('Password must be at least 8 characters', 'register')
            is_valid = False

        if not EMAIL_REGEX.match(data['email']):
            flash('Invalid email', 'register')
            is_valid = False

        if data['password'] != data['confirm_pw']:
            flash('Confirm password must match', 'register')
            is_valid = False

        if User.get_by_email(data['email']): 
            flash('Email is already registered', 'register')
            is_valid = False

        return is_valid
    
    @staticmethod
    def validate_login(form_data):
        is_valid = True

        potential_user = User.get_by_email(form_data['email'])

        if not potential_user:
            flash('Invalid email/password', 'login')
            is_valid = False
        else:
            if not Bcrypt.check_password_hash(potential_user.password, form_data['password']):
                flash('Invalid email/password', 'login')
                is_valid = False

        return is_valid