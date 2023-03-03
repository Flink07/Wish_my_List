# the model will TALK to the DATABASE
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
from flask_app.models import restaurant_model
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 



class User:
    def __init__(self, data):
        self.id = data['id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.password = data['password']

#-- create a user --
# Note: All Methods are class Methods
    @classmethod
    def create(cls, data):
        query = """
            INSERT INTO users (first_name, last_name, email, password)
            Values (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data)


    @classmethod
    def get_by_id(cls, data):
        # NOTE: this query should return a list  that we will call results 
        query = """
            SELECT * FROM users
            LEFT JOIN restaurants
            ON users.id = restaurants.user_id
            WHERE users.id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        # print(results)
        if results:
            restaurant_list = []   #makes a list of recipes in user
            this_user_instance = cls(results[0])     #instance of a User
            for row in results:
                restaurant_data = {
                    **row,
                    'id' : row['restaurants.id'],
                    'created_at' : row['created_at'],
                    'updated_at' : row['updated_at']
                }
                this_restaurant_instance = restaurant_model.Restaurant(restaurant_data) # Recipe instance
                restaurant_list.append(this_restaurant_instance)
            this_user_instance.restaurants = restaurant_list
            return this_user_instance
        return False



    # ============= GET USER BY EMAIL ===========================
    @classmethod
    def get_by_email(cls, data):
        # NOTE: this query should return a list  that we will call results 
        query = """
            SELECT * FROM users
            WHERE email = %(email)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        # print(results)
        if len(results) < 1:
            return False
        return cls(results[0])


    # * -------------- VALIDATIONS ------------------------------
    @staticmethod
    def validate(data):
        is_valid = True

        if len(data['first_name']) < 2:
            is_valid = False
            flash('first_name required', 'reg')

        if len(data['last_name']) < 2:
            is_valid = False
            flash('last_name required', 'reg')

        if len(data['email']) < 1:
            is_valid = False
            flash('email required', 'reg')
        elif not EMAIL_REGEX.match(data['email']):
            flash('Invalid email address!', 'reg')
            is_valid = False
        else:
            email_dict = {
                'email': data['email']
            }
            potential_user = User.get_by_email(email_dict)
            if potential_user:
                is_valid = False
                flash("email already taken, please input a different E-mail or log in", "reg")

        if len(data['password']) < 8:
            is_valid = False
            flash('password required and must be 8 characters', 'reg')
        elif not data['password'] == data['confirm_password']:
            is_valid = False
            flash("passwords don't match!", 'reg')

        return is_valid