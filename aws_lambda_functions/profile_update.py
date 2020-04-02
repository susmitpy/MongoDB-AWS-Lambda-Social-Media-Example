"""
Created on Fri Jun 21 22:43:57 2019

@author: susmitvengurlekar
"""

import mongoengine as mongo
from classes import Users, UserDetails
import os

class Interface:
    def __init__(self):
        self.conn = mongo.connect(host = f"mongodb+srv://{os.environ['un']}:{os.environ['pw']}@cluster0-hlox9.mongodb.net/test?retryWrites=true&w=majority")
        self.user = False
        print("Connection:", self.conn)

    def login(self, un:str) -> Users:
        user = Users.objects.get(cognito_id=un)
        if user:
            self.user = user
    
    def check_connect(self):
        try:
            mongo.get_connection()
        except mongo.connection.MongoEngineConnectionError:
            self.conn = mongo.connect(host = f"mongodb+srv://{os.environ['un']}:{os.environ['pw']}@cluster0-hlox9.mongodb.net/test?retryWrites=true&w=majority")
            self.user=False
            
    def update_details(self, name,birth_year, male, about,number,pp,public):
        details = UserDetails(name=name,birth_year=birth_year,male=male,about=about,email=self.user.details.email,number=number,public=public)
        if pp != "":
            details.pp=pp   
        self.user.details = details
        self.user.save()
        return {"oid":str(self.user.id)}


inf = Interface()

def lambda_handler(event,context):
    inf.check_connect()
    cognito_id = event["cognito_id"]
    inf.login(cognito_id)
    name = event["name"]
    birth_year = event["birth_year"]
    male = event["male"]
    about = event["about"]
    number = event["number"]
    pic = event["pic"]
    public =  event["public"]

    return inf.update_details(name,birth_year,male,about,number,pic,public)
