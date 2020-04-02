#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 14:45:50 2019

@author: susmitvengurlekar
"""

import mongoengine as mongo
from classes import Users
import os

class Interface:
    def __init__(self):
        self.conn = mongo.connect(host = f"mongodb+srv://{os.environ['un']}:{os.environ['pw']}@cluster0-hlox9.mongodb.net/test?retryWrites=true&w=majority")
        self.user = False
        
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
    def follow_request(self, to_doc_id):
         user1 = Users.objects.get(id=to_doc_id)
         self.user.following.outgoing_requests.append(user1.id)
         user1.followers.incoming_requests.append(self.user.id)
         self.user.save(validate=False) # TODO
         user1.save(validate=False) # TODO

inf = Interface()

def lambda_handler(event, context):
    inf.check_connect()
    cognito_id = event["cognito_id"]
    inf.login(cognito_id)
    to_doc_id = event["to_id"]
    inf.follow_request(to_doc_id)

