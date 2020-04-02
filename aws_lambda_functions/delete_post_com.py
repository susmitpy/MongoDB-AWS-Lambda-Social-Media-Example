#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 15:10:56 2019

@author: susmitvengurlekar
"""

import mongoengine as mongo
from classes import Community #, Users
import os

class Interface:
    def __init__(self):
        self.conn = mongo.connect(host = f"mongodb+srv://{os.environ['un']}:{os.environ['pw']}@cluster0-hlox9.mongodb.net/test?retryWrites=true&w=majority")
        self.user = False
        
#    def login(self, un:str) -> Users:
#         user = Users.objects.get(cognito_id=un)
#         if user:
#             self.user = user
    def check_connect(self):
        try:
            mongo.get_connection()
        except mongo.connection.MongoEngineConnectionError:
            self.conn = mongo.connect(host = f"mongodb+srv://{os.environ['un']}:{os.environ['pw']}@cluster0-hlox9.mongodb.net/test?retryWrites=true&w=majority")
            self.user=False
    def delete_post_in_com(self, comm_id, comm_post_id):
        Community.objects.filter(id=comm_id,posts__id=comm_post_id).update(pull__posts__id=comm_post_id)

inf = Interface()

def lambda_handler(event, context):
    inf.check_connect()
#    cognito_id = event["cognito_id"]
 #   inf.login(cognito_id)
    c_id = event["comm_id"]
    cm_p_id = event["comm_p_id"]
    inf.delete_post_in_com(c_id,cm_p_id)