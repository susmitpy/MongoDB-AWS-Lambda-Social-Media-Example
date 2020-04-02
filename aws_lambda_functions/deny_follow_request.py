#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 14:45:50 2019

@author: susmitvengurlekar
"""

import mongoengine as mongo
from classes import Users
import os
from bson import ObjectId

class Interface:
    def __init__(self):
        self.conn = mongo.connect(host = f"mongodb+srv://{os.environ['un']}:{os.environ['pw']}@cluster0-hlox9.mongodb.net/test?retryWrites=true&w=majority")
        self.user = False
        
    def login(self, un:str) -> Users:
         if not self.user:
             user = Users.objects.get(cognito_id=un)
             if user:
                 self.user = user
    def check_connect(self):
        try:
            mongo.get_connection()
        except mongo.connection.MongoEngineConnectionError:
            self.conn = mongo.connect(host = f"mongodb+srv://{os.environ['un']}:{os.environ['pw']}@cluster0-hlox9.mongodb.net/test?retryWrites=true&w=majority")
            self.user=False
    def deny_follow_request(self,of_id):
        self.user.followers.incoming_requests.remove(ObjectId(of_id))
        self.user.save()
        Users.objects(id=of_id).update_one(pull__following__outgoing_requests=self.user.id)

inf = Interface()

def lambda_handler(event, context):
    inf.check_connect()
    cognito_id = event["cognito_id"]
    inf.login(cognito_id)
    of_id = event["of_id"]
    inf.deny_follow_request(of_id)


