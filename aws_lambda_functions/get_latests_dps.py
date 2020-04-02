#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 15:17:19 2019

@author: susmitvengurlekar
"""

import mongoengine as mongo
from classes import Users,DirectChat
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
    def get_latest_direct_posts(self,direct_chat_id):
        dc = DirectChat.objects.get(id=direct_chat_id)
        if not self.user.id in dc.between:
            return {"res":"fraud"}
        dps = dc.chat_log.filter(fetched=False)
        res = {}
        for i,dp in enumerate(dps):
            dp.fetched=True
            res_part = {
                "from_id":dp.from_id,
                "text":dp.text,
                "font_size":dp.font_size,
                "id":dp.id
                }
            if "media_link" in dp:
                res_part["media_link"] = dp.media_link
            res[i] = res_part
        dc.chat_log.save()
        return res

inf = Interface()

def lambda_handler(event, context):
    inf.check_connect()
    cognito_id = event["cognito_id"]
    inf.login(cognito_id)
    dc_id = event["dc_id"]
    return inf.get_latest_direct_posts(dc_id)