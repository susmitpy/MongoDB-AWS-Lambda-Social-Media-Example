#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 14:54:38 2019

@author: susmitvengurlekar
"""

import mongoengine as mongo
from classes import Users, UserDetails, ConnectionDetails, Field, Community, CommunityDetails, ComPost, DirectChat, DirectPost, ProfilePost,Followers,Following
import json
import os
from datetime import datetime
import bson
from bson import ObjectId

os.environ["un"] = "susmit"
os.environ["pw"] = "userSusmit03"

class Interface:
    def __init__(self):
        self.conn = mongo.connect(host = f"mongodb+srv://{os.environ['un']}:{os.environ['pw']}@cluster0-hlox9.mongodb.net/test?retryWrites=true&w=majority")
        self.user = False
        print("Connection:", self.conn)
        
# ==================================USERS===========================================
    def register(self, cognito:str, email) -> bool:
         user = Users.objects(cognito_id=cognito)
         print("In register")
         if user:
             return False
         det = UserDetails(email=email,tags=[])
         user = Users(cognito_id=cognito, details = det,followers=Followers(),following=Following(),direct_chats=[],reporters_members=[],viewers=[],communities=[],profile_posts=[],blocked=[])
         user.save()
         return True
     
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
            
    def disconnect(self):
        mongo.disconnect()

     
    def details(self):
         print(f"""
               Document id: {self.user.id}
               Cognito id: {self.user.cognito_id}    
               """)
         
    def view_user(self, viewed_user_id):
        user = Users.objects.get(id=viewed_user_id)
        user.views += 1
        if not self.user.id in user.details.viewers:
            user.viewers.append(self.user.id)
        user.save()

    
    def block_report_user(self,user_id):
        user_to_be_reported = Users.objects.get(id=user_id)
        if not self.user.id in user_to_be_reported.reporters_members:
            user_to_be_reported.reporters_members.append(self.user.id)
        user_to_be_reported.save()
        if user_id not in self.user.blocked:
            self.user.blocked.append(user_id)
            self.user.save()
    
    
    def create_profile_post(self,text,public,media_link=None):
        if media_link:
            pp = ProfilePost(text=text,media_link=media_link,public=public)
        else:
            pp = ProfilePost(text=text,public=public)
        
        self.user.profile_posts.append(pp)
        self.user.save()
        return {"pp_id":pp.id}
    
    def update_details(self, name,birth_year, male, about,number,pp,public):
        details = UserDetails(name=name,birth_year=birth_year,male=male,about=about,email=self.user.details.email,number=number,pp = pp,public=public)
        self.user.details = details
        self.user.save()
        return {"oid":str(self.user.id)}
    
    def update_selective_details(self, details):
        j = self.user.details.to_json()
        for k,v in details.items():
            if k in j:
                setattr(self.user.details,k,v)
                if k == "pp":
                    self.user.details.pp_last_updated = datetime.now()
        self.user.save()
    
    def get_self_details(self):
        return json.loads(self.user.details.to_json())

    def get_details(self, of_id):
        if of_id == "":
            return json.loads(self.user.details.to_json())
        else:
            user = Users.objects.get(id=of_id)
            return json.loads(user.details.to_json())
    
    def get_prof_details(self,of_id):
        user = Users.objects.get(id=of_id)
        j = json.loads(user.details.to_json())
        keys = ["name","about","pp"]
        res = {i:j for i,j in zip(keys,[j[k] for k in keys])}
        return res
    
    def get_direct_chats(self):
        dcs = self.user.direct_chats
        res = {}
        for i,dc in enumerate(dcs):
            res[i]=dc.to_json()
        return res
    
    def get_profile_posts(self):
        pps = self.user.profile_posts
        res = {}
        for i,pp in enumerate(pps):
            res[i]=pp.to_json()
        return res
    
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
    
    def get_users_by_un(self,un):
        users = Users.objects(details__un__icontains=un)
        res = {}
        for i,user in enumerate(users):
            res_part={}
            res_part["id"] = user.id
            res_part["name"] = user.details.name
            res_part["un"]=user.details.un
            res_part["pp"] = user.details.pp
            res_part["email"] = user.details.email
            res_part["about"] = user.details.about
            res[i] = res_part
        return res
    
    def delete_profile_post(self,pp_id):
        self.user.update(pull_profile_posts__id=pp_id)
        self.user.save()
        
        
# ================================Chats=============================================

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
    
    def post_in_old_direct_chat(self,text,direct_chat_id,media_link=None):
        dc = DirectChat.objects.get(id=direct_chat_id)
        if media_link:
            chat = DirectPost(from_id = self.user.id,text=text,media_link=media_link)
        else:
            chat = DirectPost(from_id = self.user.id,text=text)
        dc.chat_log.append(chat)
        dc.save()
        return {"dp_id":chat.id}
    
    def delete_post_in_direct_chat(self,dc_id,dp_id):
        dc = DirectChat.objects.get(id=dc_id)
        dc.update(pull__chat_log__id=dp_id)
        dc.save()
        
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
    
    def get_latest_direct_posts_by_id(self,dc_id,last_dp_id):
        last_dp_obj_id = ObjectId(last_dp_id)
        dc = DirectChat.objects.get(id=dc_id)
        dps = dc.chat_log
        i = 0
        res = {}
        for dp in reversed(dps):
            if last_dp_obj_id < ObjectId(dp.id):
                res_part = {
                "from_id":dp.from_id,
                "text":dp.text,
                "font_size":dp.font_size,
                "id":dp.id
                }
                if "media_link" in dp:
                    res_part["media_link"] = dp.media_link
                res[i] = res_part
                i+=1
            else:
                break
        return res
                
        
    def delete_direct_chat(self,dc_id):
        dc = DirectChat.objects.get(id=dc_id)
        self.user.direct_chats.remove(dc)
        if dc.del_by_one:
            dc.delete()
        else:
            dc.del_by_one = True
        dc.save()
        self.user.save()

# =============================================================================

    

# =================================CONNECTIONS=========================================
    
     
    def get_incoming_requests(self):
         return self.user.followers.incoming_requests
     
    def get_outgoing_requests(self):
        return self.user.followers.outgoing_requests
    
    
    def follow_request(self, to_doc_id):
         user1 = Users.objects.get(id=to_doc_id)
         self.user.following.outgoing_requests.append(user1.id)
         user1.followers.incoming_requests.append(self.user.id)
         self.user.save(validate=False) # TODO
         user1.save(validate=False) # TODO
     
    def accept_request(self, from_doc_id):
         con1 = self.user.followers;
         user1 = Users.objects.get(id=from_doc_id)
         con1.active.append(ConnectionDetails(with_id=con1.incoming_requests.pop(con1.incoming_requests.index(user1.id))))
         con2 = user1.following
         con2.active.append(ConnectionDetails(with_id=con2.outgoing_requests.pop(con2.outgoing_requests.index(self.user.id))))
         self.user.save(validate=False)  # TODO
         user1.save()
     
    def get_active_followers(self, user_id=""):
         if user_id == "":
             return [con.with_id for con in self.user.followers.active]
         user1 = Users.objects.get(id=user_id)
         return [con.with_id for con in user1.followers.active if con.public]
     
    def get_active_following(self, user_id=""):
         if user_id == "":
             return [con.with_id for con in self.user.following.active]
         user1 = Users.objects.get(id=user_id)
         return [con.with_id for con in user1.following.active if con.public]
     
    def deny_follow_request(self,of_id):
        self.user.followers.incoming_requests.remove(bson.ObjectId(of_id))
        self.user.save()
        Users.objects(id=of_id).update_one(pull__following__outgoing_requests=self.user.id)

    def unfollow(self,whom_id):
        self.user.update_one(pull__following__active__with_id=whom_id)
        Users.objects(id=whom_id).update_one(pull__followers__active__with_id=self.user.id)

    def remove_follower(self,followers_id):
        self.user.update_one(pull__followers__active__with_id=followers_id)
        Users.objects(id=followers_id).update_one(pull__following__active__with_id=self.user.id)
# =============================================================================
    
 
    

# ================================COMMUNITIES=========================================
    def create_new_field(self,title):
         details = CommunityDetails(title=title, country="world")
         comm = Community(details=details)
         comm.save()
         communities={"world":comm.to_dbref()}
         field = Field(title=title, communities=communities)
         field.save()
     
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
        
    def create_com_post(self,comm_id,text,media_link=None):
            p = ComPost(from_id = self.user.id, text=text,media_link=media_link)
            c = Community.objects.get(id=comm_id)
            c.posts.append(p)
            c.save()
            return p.id
            
    def delete_post_in_com(self, comm_id, comm_post_id):
        Community.objects.filter(id=comm_id,posts__id=comm_post_id).update(pull__posts__id=comm_post_id)
        
    def report_com_post(self,comm_id,comm_post_id):
        Community.objects.filter(id=comm_id,posts__id=comm_post_id).update(push__posts__S__reporters_members=self.user.id)
        

# =============================================================================
    
# ===================================Feeds==========================================
    
# =============================================================================
