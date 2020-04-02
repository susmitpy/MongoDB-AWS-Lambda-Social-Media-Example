#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 14:44:00 2019

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
    def get_direct_chats(self):
        dcs = self.user.direct_chats
        res = {}
        for i,dc in enumerate(dcs):
            res[i]=dc.to_json()
        return res

inf = Interface()

def lambda_handler(event, context):
    inf.check_connect()
    cognito_id = event["cognito_id"]
    inf.login(cognito_id)
    return inf.get_direct_chats()
        
    
    
    