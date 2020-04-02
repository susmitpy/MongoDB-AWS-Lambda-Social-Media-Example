#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 15:10:56 2019

@author: susmitvengurlekar
"""

import mongoengine as mongo
from classes import Users, DirectChat, DirectPost
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
    def create_new_direct_chat(self,text,to_id,media_link=None):
        # TODO
        # Only if to_id follows self.user.id
        if media_link:
            chat = DirectPost(from_id = self.user.id,text=text,media_link=media_link)
        else:
            chat = DirectPost(from_id = self.user.id,text=text)
        dc = DirectChat(chat_log = [chat], between=[self.user.id,to_id])
        dc.save(validate=False) # TODO
        user1 = Users.objects.get(id=to_id)
        user1.direct_chats.append(dc.to_dbref())
        self.user.direct_chats.append(dc.to_dbref())
        self.user.save()
        user1.save()
        return {"dc_id":dc.id,"dp_id":chat.id}

inf = Interface()

def lambda_handler(event, context):
    inf.check_connect()
    cognito_id = event["cognito_id"]
    inf.login(cognito_id)
    text = event["text"]
    to_id = event["to_object_id"]
    if "media_link" in event:
        return inf.create_new_direct_chat(text,to_id,event["media_link"])
    else:
        return inf.create_new_direct_chat(text,to_id)