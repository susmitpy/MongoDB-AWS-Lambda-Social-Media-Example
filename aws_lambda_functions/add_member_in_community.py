#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 14:45:50 2019

@author: susmitvengurlekar
"""

import mongoengine as mongo
from classes import Users, CommunityDetails, Community, Field
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
    def add_member(self,field_id,country):
        f = Field.objects.get(id=field_id)
        commu = f.communities.get(country)
        if commu:
            commu.members.append(self.user.to_dbref())
            commu.save()
            self.user.communitites.append(commu.id)
        else:
            details = CommunityDetails(title=f.title,country=country)
            commu = Community(details=details, members=[self.user.to_dbref()])
            commu.save()
            f.communities[country] = commu.to_dbref()
            f.save()
            self.user.communitites.append(commu.id)
        self.user.save()
        return commu.to_json()
inf = Interface()

def lambda_handler(event, context):
    inf.check_connect()
    cognito_id = event["cognito_id"]
    inf.login(cognito_id)
    f_id = event["field_id"]
    country = event["country"]
    return inf.add_member(f_id,country)

