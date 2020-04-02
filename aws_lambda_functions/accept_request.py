#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 14:45:50 2019

@author: susmitvengurlekar
"""

import mongoengine as mongo
from classes import Users, ConnectionDetails
import os

class Interface:
    def __init__(self):
        self.conn = mongo.connect(host = f"mongodb+srv://{os.environ['un']}:{os.environ['pw']}@cluster0-hlox9.mongodb.net/test?retryWrites=true&w=majority")
        self.user = False
        
    def login(self, un:str) -> Users:
         if not self.user:
             user = Users.objects.get(cognito_id=un)
             if user:
                 self.user = user
    def check_connect(self):
        try:
            mongo.get_connection()
        except mongo.connection.MongoEngineConnectionError:
            self.conn = mongo.connect(host = f"mongodb+srv://{os.environ['un']}:{os.environ['pw']}@cluster0-hlox9.mongodb.net/test?retryWrites=true&w=majority")
            self.user=False
    def accept_request(self, from_doc_id):
         con1 = self.user.followers;
         user1 = Users.objects.get(id=from_doc_id)
         con1.active.append(ConnectionDetails(with_id=con1.incoming_requests.pop(con1.incoming_requests.index(user1.id))))
         con2 = user1.following
         con2.active.append(ConnectionDetails(with_id=con2.outgoing_requests.pop(con2.outgoing_requests.index(self.user.id))))
         self.user.save(validate=False)  # TODO
         user1.save()

inf = Interface()

def lambda_handler(event, context):
    inf.check_connect()
    cognito_id = event["cognito_id"]
    inf.login(cognito_id)
    from_doc_id = event["from_id"]
    inf.accept_request(from_doc_id)

