from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
from flask_app.models import user_model



class Restaurant:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.type = data['type']
        self.address = data['address']
        self.description = data['description']
        self.recommendation = data['recommendation']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']


#=======================Create==================================
    @classmethod
    def create(cls, data):
        query="""
            INSERT INTO restaurants (name, type, address, description, recommendation, user_id)
            VALUES (%(name)s, %(type)s, %(address)s, %(description)s, %(recommendation)s, %(user_id)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data)

#=================READ ALL - DISPLAY ON DASHBOARD===============
    @classmethod
    def get_all(cls):
        query = """
            SELECT * FROM restaurants
            JOIN users
            ON restaurants.user_id = users.id;
        """
        results = connectToMySQL(DATABASE).query_db(query)
        all_restaurants = []
        if results:
            for row in results:
                this_restaurant = cls(row)
                user_data = {
                    'id' : row['users.id'],
                    'created_at' : row['users.created_at'],
                    'updated_at' : row['users.updated_at'],
                    **row
                }
                this_user = user_model.User(user_data)
                this_restaurant.creator = this_user
                all_restaurants.append(this_restaurant)
        return all_restaurants



#======================  READ ONE  ===============================
    @classmethod
    def get_by_id(cls, data):
        query = """
            SELECT * FROM restaurants
            JOIN users
            ON restaurants.user_id = users.id
            WHERE restaurants.id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            this_restaurant = cls(results[0])
            row = results[0]
            user_data = {
               **row,
                'id': row['users.id'],
                'created_at' : row['users.created_at'],
                'updated_at' : row['users.updated_at'] 
            }
            this_user = user_model.User(user_data)
            this_restaurant.creator = this_user
            return this_restaurant
        return False

#=====================  UPDATE - EDIT  ==================================
    @classmethod
    def update(cls, data):
        query = """
            UPDATE restaurants
            SET
            name = %(name)s,
            type = %(type)s,
            address = %(address)s,
            description = %(description)s,
            recommendation = %(recommendation)s
            WHERE id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query, data)
#=====================  DELETE   ==================================
    @classmethod
    def delete(clas, data):
        query = """
            DELETE from restaurants
            WHERE id = %(id)s
        """
        return connectToMySQL(DATABASE).query_db(query, data)


#===================  VALIDATIONS ==================================
    @staticmethod
    def validate(form_data):
        is_valid = True

        if len(form_data['name']) < 1:
            is_valid = False
            flash('name must have at least 1 Character')
        
        if len(form_data['type']) < 3:
            is_valid = False
            flash('type must have at least 1 Character')

        if len(form_data['address']) < 5:
            is_valid = False
            flash('address date is required')

        if len(form_data['description']) < 3:
            is_valid = False
            flash('Description  Must not be blank')

        return is_valid
