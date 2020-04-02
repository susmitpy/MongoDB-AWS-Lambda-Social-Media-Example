
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 15:14:48 2019

@author: susmitvengurlekar
"""

import mongoengine as mongo
from classes import Users,DirectChat,DirectPost
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
    
    def post_in_old_direct_chat(self,text,direct_chat_id,media_link=None):
        dc = DirectChat.objects.get(id=direct_chat_id)
        if media_link:
            chat = DirectPost(from_id = self.user.id,text=text,media_link=media_link)
        else:
            chat = DirectPost(from_id = self.user.id,text=text)
        dc.chat_log.append(chat)
        dc.save()
        return {"dp_id":chat.id}

inf = Interface()

def lambda_handler(event, context):
    def check_connect(self):
        try:
            mongo.get_connection()
        except mongo.connection.MongoEngineConnectionError:
            self.conn = mongo.connect(host = f"mongodb+srv://{os.environ['un']}:{os.environ['pw']}@cluster0-hlox9.mongodb.net/test?retryWrites=true&w=majority")
            self.user=False
    cognito_id = event["cognito_id"]
    inf.login(cognito_id)
    text = event["text"]
    dc_id = event["dc_id"]
    if "media_link" in event:
        return inf.post_in_old_direct_chat(text,dc_id,event["media_link"])
    else:
        return inf.post_in_old_direct_chat(text,dc_id)