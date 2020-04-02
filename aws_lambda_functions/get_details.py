#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 16:06:04 2019

@author: susmitvengurlekar
"""

"""
Created on Fri Jun 21 14:54:38 2019

@author: susmitvengurlekar
"""

import json
import mongoengine as mongo
from classes import Users
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
    def get_details(self, of_id):
        if of_id == "":
            return json.loads(self.user.details.to_json())
        else:
            user = Users.objects.get(id=of_id)
            return json.loads(user.details.to_json())

inf = Interface()

def lambda_handler(event, context):
    inf.check_connect()
    cognito_id = event["cognito_id"]
    inf.login(cognito_id)
    of_id = event["of_id"]
    return {
        'statusCode': 200,
        'body': inf.get_details(of_id)
    }
