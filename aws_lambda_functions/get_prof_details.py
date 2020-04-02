#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Fri Jun 21 14:54:38 2019

@author: susmitvengurlekar
"""

import mongoengine as mongo
from classes import Users
import json
import os

class Interface:
    def __init__(self):
        self.conn = mongo.connect(host = f"mongodb+srv://{os.environ['un']}:{os.environ['pw']}@cluster0-hlox9.mongodb.net/test?retryWrites=true&w=majority")
        self.user = False
        
#    def login(self, un:str) -> Users:
#        user = Users.objects.get(cognito_id=un)
#        if user:
#            self.user = user
    def check_connect(self):
        try:
            mongo.get_connection()
        except mongo.connection.MongoEngineConnectionError:
            self.conn = mongo.connect(host = f"mongodb+srv://{os.environ['un']}:{os.environ['pw']}@cluster0-hlox9.mongodb.net/test?retryWrites=true&w=majority")
            self.user=False         
    def get_prof_details(self,of_id):
        user = Users.objects.get(id=of_id)
        j = json.loads(user.details.to_json())
        keys = ["name","about","pp"]
        res = {i:j for i,j in zip(keys,[j[k] for k in keys])}
        return res
   
inf = Interface() 

def lambda_handler(event, context):
    inf.check_connect()
#    cognito_id = event["cognito_id"]
#    inf.login(cognito_id)
    of_id = event["of_id"]
    return {
        'statusCode': 200,
        'body': inf.get_prof_details(of_id)
    }
