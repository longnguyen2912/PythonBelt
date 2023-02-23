from flask_app.config.mysqlconnection import connectToMySQL
import re 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash
from flask_app.models import user

class Sighting:
    db = "belt_schema"
    def __init__(self, data):
        self.id = data['id']
        self.location = data['location']
        self.happnened = data['happened']
        self.date = data['date']
        self.NumOfSas = int(data['NumOfSas'])
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO sightings (location,happened,date,NumOfSas,user_id) VALUES(%(location)s,%(happened)s,%(date)s,%(NumOfSas)s,%(user_id)s)"
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM sightings JOIN users ON users.id = sightings.user_id;"
        results = connectToMySQL(cls.db).query_db(query)
        all_sightings = []
        for row in results:
            instance = cls(row)
            user_data = {
                **row,
                'id' : row['users.id'],
                'created_at' : row['users.created_at'],
                'updated_at' : row['users.updated_at']
            }
            user_instance = user.User(user_data)
            instance.user = user_instance
            all_sightings.append(instance)
        return all_sightings
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM sightings WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls( results[0] )

    @classmethod
    def update(cls, data):
        query = "UPDATE sightings SET location=%(location)s, happened=%(happened)s, date=%(date)s, NumOfSas=%(NumOfSas)s, user_id=%(user_id)s ,updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def delete(cls,data):
        query = "DELETE FROM sightings WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)


    @staticmethod
    def validate_sighting(sighting):
        is_valid = True
        if len(sighting['location']) < 3:
            flash("Location must be at least 3 characters","sighting")
            is_valid=False
        if len(sighting['happened']) < 10:
            flash("Type at least 10 characters about what happened","sighting")
            is_valid=False
        if sighting['date'] == "":
            flash("Please enter a date","sighting")
            is_valid= False
        if int(sighting['NumOfSas']) < 1:
            flash("Please enter the number of Sasquatches","sighting")
            is_valid= False
        return is_valid