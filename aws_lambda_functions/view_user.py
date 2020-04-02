#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 15:19:29 2019

@author: susmitvengurlekar
"""

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
             
    def view_user(self, viewed_user_id):
        user = Users.objects.get(id=viewed_user_id)
        user.views += 1
        if not self.user.id in user.details.viewers:
            user.viewers.append(self.user.id)
        user.save()

inf = Interface()

def lambda_handler(event, context):
    inf.check_connect()
    cognito_id = event["cognito_id"]
    inf.login(cognito_id)
    viewed_user_object_id = event["viewed_user_id"]
    inf.view_user(viewed_user_object_id)