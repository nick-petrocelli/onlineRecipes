from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.__init__ import DATABASE
from flask_app.models.user import User
from flask import flash


class Recipe:
    def __init__( self , data ): 
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under = data['under']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.owner_id = data['owner_id']
        self.owner = None

    @staticmethod
    def validate_recipe(data):
        is_valid = True

        if len(data['name']) < 3:
            flash('Name must be at least 3 characters')
            is_valid = False

        if len(data['description']) < 3:
            flash('Description must be at least 3 characters')
            is_valid = False

        if len(data['instructions']) < 3:
            flash('Instructions must be at least 3 characters')
            is_valid = False
            
        if len(data['date_made']) < 1:
            flash('Date is required')
            is_valid = False

        if not 'under' in data:
            flash('Please pick if cook time is under 30 minutes')
            is_valid = False

        return is_valid
    
    @classmethod
    def save(cls, form_data):
        query = '''
            INSERT INTO recipes (name, description, instructions, date_made, under, owner_id)
            VALUES (%(name)s, %(description)s, %(instructions)s, %(date_made)s, %(under)s, %(owner_id)s)
        '''
        recipe_id = connectToMySQL(DATABASE).query_db(query, form_data)
        return recipe_id
    
    @classmethod
    def edit_one(cls, form_data):
        query = '''
            UPDATE recipes
            SET name = %(name)s ,
            description = %(description)s ,
            instructions = %(instructions)s ,
            date_made = %(date_made)s ,
            under = %(under)s
            WHERE id = %(id)s;
        '''
        connectToMySQL(DATABASE).query_db(query, form_data)
        return True
    
    @classmethod
    def delete_recipe(cls, id):
        id_dict = {'id' : id}
        query = '''
            DELETE FROM recipes WHERE id = %(id)s
        '''
        connectToMySQL(DATABASE).query_db(query, id_dict)
        return True
    
    @classmethod
    def get_all_with_owner(cls):
        query = '''
            SELECT * FROM recipes
            LEFT JOIN users ON recipes.owner_id = users.id
        '''
        results = connectToMySQL(DATABASE).query_db(query)
        recipes = []
        for row in results:
            each_recipe = cls(row)
            user_dict = {
                'id' : row['users.id'],
                'first_name' : row['first_name'],
                'last_name' : row['last_name'],
                'password' : row['password'],
                'email' : row['email'],
                'created_at' : row['users.created_at'],
                'updated_at' : row['users.updated_at'],
            }
            user_from_row = User(user_dict)
            each_recipe.owner = user_from_row
            recipes.append(each_recipe)

        return recipes
    
    @classmethod
    def get_one_with_owner(cls, id):
        id_dict = {'id' : id}
        query = '''
            SELECT * FROM recipes
            LEFT JOIN users ON recipes.owner_id = users.id
            WHERE recipes.id = %(id)s;
        '''
        results = connectToMySQL(DATABASE).query_db(query, id_dict)
        row = results[0]

        recipe = cls(row)
        user_dict = {
            'id' : row['users.id'],
            'first_name' : row['first_name'],
            'last_name' : row['last_name'],
            'password' : row['password'],
            'email' : row['email'],
            'created_at' : row['users.created_at'],
            'updated_at' : row['users.updated_at'],
        }
        recipe.owner = User(user_dict)

        return recipe
    
