#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 14:39:00 2019

@author: susmitvengurlekar
"""

import mongoengine as mongo
from classes import Users,ProfilePost
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
    def create_profile_post(self,text,public,media_link=None):
        if media_link:
            pp = ProfilePost(text=text,media_link=media_link,public=public)
        else:
            pp = ProfilePost(text=text,public=public)
        
        self.user.profile_posts.append(pp)
        self.user.save()
        return {"pp_id":pp.id}

inf = Interface()

def lambda_handler(event, context):
    inf.check_connect()
    cognito_id = event["cognito_id"]
    inf.login(cognito_id)
    text = event["text"]
    public = event["public"]
    if "media_link" in event:
        return inf.create_profile_post(text,public,event["media_link"])
    else:
        return inf.create_profile_post(text,public)
        
    
    
    