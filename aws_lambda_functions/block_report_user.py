#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 15:10:56 2019

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
    def block_report_user(self,user_id):
        user_to_be_reported = Users.objects.get(id=user_id)
        if not self.user.id in user_to_be_reported.reporters_members:
            user_to_be_reported.reporters_members.append(self.user.id)
        user_to_be_reported.save()
        if user_id not in self.user.blocked:
            self.user.blocked.append(user_id)
            self.user.save()

inf = Interface()

def lambda_handler(event, context):
    inf.check_connect()
    cognito_id = event["cognito_id"]
    inf.login(cognito_id)
    of_id = event["of_object_id"]
    inf.block_report_user(of_id)

