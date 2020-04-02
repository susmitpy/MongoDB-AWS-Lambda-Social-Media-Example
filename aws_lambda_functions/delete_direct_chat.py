#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 15:10:56 2019

@author: susmitvengurlekar
"""

import mongoengine as mongo
from classes import DirectChat, Users
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
    def delete_direct_chat(self,dc_id):
        dc = DirectChat.objects.get(id=dc_id)
        self.user.direct_chats.remove(dc)
        if dc.del_by_one:
            dc.delete()
        else:
            dc.del_by_one = True
        dc.save()
        self.user.save()

inf = Interface()

def lambda_handler(event, context):
    inf.check_connect()
    cognito_id = event["cognito_id"]
    inf.login(cognito_id)
    dc_id = event["dc_id"]
    inf.delete_direct_chat(dc_id)