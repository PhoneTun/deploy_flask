from flask_app.config.mysqlconnetions import connectToMySQL
from flask import flash
from flask_app.models.user import User
import re

DB='exam'
class Sighting:
    def __init__(self, data):
        self.id = data['id']
        self.location = data['location']
        self.what_happen = data['what_happen']
        self.date_of_siting = data['date_of_siting']
        self.no_of_sasquatchs = data['no_of_sasquatchs']
        self.user = data['user']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO sightings(location, what_happen, date_of_siting, no_of_sasquatchs,  user_id) values (%(location)s, %(what_happen)s, %(date_of_siting)s,%(no_of_sasquatchs)s, %(user_id)s);"
        results = connectToMySQL(DB).query_db(query,data)
        print (results)
        return results
    @classmethod
    def update(cls, sighting_data):
        query = '''UPDATE sightings 
            SET location=%(location)s, what_happen=%(what_happen)s, date_of_siting=%(date_of_siting)s, no_of_sasquatchs=%(no_of_sasquatchs)s
            WHERE id = %(id)s'''
        return connectToMySQL(DB).query_db(query, sighting_data)

    
    @classmethod
    def get_all(cls):
        query='''select * from sightings
        join users on sightings.user_id=users.id'''
        print("in get all method")
        results=connectToMySQL(DB).query_db(query)
        # print(">>>>>>>>>" , results)
        all_results=[]
        for result in results:
            posting_user=User({
                "id": result["users.id"],
                "first_name": result["first_name"],
                "last_name": result["last_name"],
                "email": result["email"],
                "password": result["password"],
                "created_at": result["users.created_at"],
                "updated_at": result["users.updated_at"]
            })
            new_sighitng= Sighting({
                "id": result["id"],
                "location": result["location"],
                "what_happen": result["what_happen"],
                "date_of_siting": result["date_of_siting"],
                "no_of_sasquatchs": result["no_of_sasquatchs"],
                "user": posting_user,
                "created_at": result["created_at"],
                "updated_at": result["updated_at"]
                })
            all_results.append(new_sighitng)
            print(new_sighitng.user.first_name)
        return all_results
    
    @classmethod
    def get_one(cls,sighting_id):
        query='''select * from sightings
        join users on sightings.user_id=users.id
        WHERE sightings.id = %(id)s'''
        data={'id':sighting_id}
        results=connectToMySQL(DB).query_db(query,data)
        sight_dict=results[0]
        # print("xxxxxxxxxxxxxxxxxxxxxxx", recipe_dict)

        # recipe_obj=Recipe(recipe_dict)
        posting_user=User({
                "id": sight_dict["users.id"],
                "first_name": sight_dict["first_name"],
                "last_name": sight_dict["last_name"],
                "email": sight_dict["email"],
                "password": sight_dict["password"],
                "created_at": sight_dict["users.created_at"],
                "updated_at": sight_dict["users.updated_at"]
            })
        new_sighitng= Sighting({
                "id": sight_dict["id"],
                "location": sight_dict["location"],
                "what_happen": sight_dict["what_happen"],
                "date_of_siting": sight_dict["date_of_siting"],
                "no_of_sasquatchs": sight_dict["no_of_sasquatchs"],
                "user": posting_user,
                "created_at": sight_dict["created_at"],
                "updated_at": sight_dict["updated_at"]
                })
        print(">>>>>>>>>" , new_sighitng)
        return new_sighitng
    
    @classmethod
    def get_skeptics_for_sighting(cls, sighting_id):
        query = """SELECT users.* FROM skeptics
            JOIN users ON skeptics.user_id = users.id
            WHERE skeptics.sighting_id = %(sighting_id)s;"""
        return connectToMySQL(DB).query_db(query, {'sighting_id': sighting_id})
    
    @classmethod
    def delete (cls, sighting_id):
        query='''DELETE FROM sightings WHERE id = %(id)s;'''
        return connectToMySQL(DB).query_db(query, {"id": sighting_id})

    @staticmethod
    def validate_sighting(sighting):
        isvalid = True
        if len(sighting['location']) <= 0:
            flash("location required", "create")
            isvalid = False
        if len(sighting['what_happen']) <= 0:
            flash("List what happened", "create")
            isvalid = False
        if len(sighting['date_of_siting']) <= 0:
            flash("Pick a date", "create")
            isvalid = False
        try:
            if int(sighting['no_of_sasquatchs']) <= 1:
                flash("Number of sasquatchs is missing", "create")
                isvalid = False
        except ValueError:
            flash("Invalid number format for sasquatch count", "create")
            isvalid = False
        return isvalid