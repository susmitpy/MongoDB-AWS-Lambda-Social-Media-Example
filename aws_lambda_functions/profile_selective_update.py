"""
Created on Fri Jun 21 22:43:57 2019

@author: susmitvengurlekar
"""

import mongoengine as mongo
from classes import Users
import os
from datetime import datetime

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

    def update_selective_details(self, details):
        j = self.user.details.to_json()
        for k,v in details.items():
            if k in j:
                setattr(self.user.details,k,v)
                if k == "pp":
                    self.user.details.pp_last_updated = datetime.now()
        self.user.save()


inf = Interface()

def lambda_handler(event,context):
    inf.check_connect()
    cognito_id = event["cognito_id"]
    details = event["details"]
    inf.login(cognito_id)
    return inf.update_selective_details(details)
