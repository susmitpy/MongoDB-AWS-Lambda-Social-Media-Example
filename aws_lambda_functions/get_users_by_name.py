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
    def get_users_by_name(self,name):
        users = Users.objects(details__name__icontains=name)
        res = {}
        for i,user in enumerate(users):
            res_part={}
            res_part["id"] = user.id
            res_part["name"] = user.details.name
            res_part["pp"] = user.details.pp
            res_part["email"] = user.details.email
            res_part["about"] = user.details.about
            res[i] = res_part
        return res

inf = Interface()

def lambda_handler(event, context):
    inf.check_connect()
    cognito_id = event["cognito_id"]
    inf.login(cognito_id)
    name = event["name"]
    return inf.get_users_by_name(name)