from flask_app.config.mysqlconnetions import connectToMySQL
from flask import flash
import re


DB="exam"
class Skeptic:
    def __init__(self, data):
        self.id = data['id']
        self.user = data['user']
        self.sighting = data['sighting']


    @classmethod
    def add_skeptic(cls, data):
        query = "INSERT INTO skeptics (sighting_id, user_id) VALUES (%(sighting_id)s, %(user_id)s);"
        return connectToMySQL(DB).query_db(query, data)
    


    @classmethod
    def remove_skeptic(cls, data):
        query = "DELETE FROM skeptics WHERE sighting_id = %(sighting_id)s AND user_id = %(user_id)s;"
        return connectToMySQL(DB).query_db(query, data)

    @classmethod
    def get_skeptics_for_sighting(cls, sighting_id):
        query = """SELECT users.* FROM skeptics
            JOIN users ON skeptics.user_id = users.id
            WHERE skeptics.sighting_id = %(sighting_id)s;"""
        return connectToMySQL(DB).query_db(query, {'sighting_id': sighting_id})