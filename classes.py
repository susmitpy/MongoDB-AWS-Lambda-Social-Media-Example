#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 22:43:57 2019

@author: susmitvengurlekar
"""
import mongoengine as mongo
from bson.objectid import ObjectId
from datetime import datetime


class ConnectionDetails(mongo.EmbeddedDocument):
    public = mongo.BooleanField(default=True)
    with_id = mongo.ObjectIdField()
      
class Connections(mongo.EmbeddedDocument):
    active = mongo.EmbeddedDocumentListField(document_type=ConnectionDetails)
    incoming_requests = mongo.ListField(mongo.ObjectIdField())
    outgoing_requests = mongo.ListField(mongo.ObjectIdField())
    meta = {'allow_inheritance': True}
    
class Followers(Connections):
    pass

class Following(Connections):
    important_daily_update = mongo.BooleanField(default=False)
 

# =============================POSTS================================================

class Post(mongo.EmbeddedDocument):
    id = mongo.ObjectIdField(default=ObjectId)
    text = mongo.StringField()
    media_link = mongo.URLField()
    # TODO to remove
    fetched = mongo.BooleanField(default=False)
    from_id = mongo.ObjectIdField()
    meta = {'allow_inheritance': True}

class DirectPost(Post):
    font_size = mongo.IntField(min_value=10,max_value=20, default=10)
    
class ComPost(Post):
    reporters_members = mongo.ListField(field=mongo.ObjectIdField())
    reporters = mongo.IntField(min_value=0)

class ProfilePost(Post):
    views = mongo.IntField(min_value=0)
    public = mongo.BooleanField(default=False)
    

class FeedPost(Post):
    views = mongo.IntField(min_value=0)
    likes = mongo.IntField(min_value=0)
    shares = mongo.IntField(min_value=0)
    
    
    
# =============================================================================

class Feeds(mongo.Document):
    of = mongo.ObjectIdField()
    tags = mongo.ListField(mongo.StringField())
    posts = mongo.EmbeddedDocumentListField(FeedPost)
   
class DirectChat(mongo.Document):
    chat_log = mongo.EmbeddedDocumentListField(document_type=DirectPost)
    between = mongo.ListField(mongo.ObjectIdField())
    del_by_one = mongo.BooleanField(default=False)
    
    

class UserDetails(mongo.EmbeddedDocument): 
        name = mongo.StringField()
        un = mongo.StringField()
        birth_year = mongo.IntField()
        email = mongo.EmailField()
        pp = mongo.URLField(default="https://flyer-user-profile.s3.ap-south-1.amazonaws.com/default_account_icon.png")
        pp_last_updated = mongo.DateTimeField(default=datetime.now())
        male = mongo.BooleanField()
        about = mongo.StringField()
        number = mongo.StringField()
        public = mongo.BooleanField(default=False)
        tags = mongo.ListField(mongo.StringField())
        country = mongo.StringField()
        
    
class Users(mongo.Document): 
     cognito_id = mongo.StringField(required=True,unique=True)
     details = mongo.EmbeddedDocumentField(UserDetails)
     followers = mongo.EmbeddedDocumentField(Followers)
     following = mongo.EmbeddedDocumentField(Following)
     direct_chats = mongo.ListField(mongo.ReferenceField(DirectChat))
     reporters_members = mongo.ListField(mongo.ObjectIdField())
     views = mongo.IntField(default=0)
     viewers = mongo.ListField(mongo.ObjectIdField())
     communities = mongo.ListField(mongo.ObjectIdField())
     profile_posts = mongo.EmbeddedDocumentListField(ProfilePost)
     feed_posts = mongo.EmbeddedDocumentListField(FeedPost)
     feed = mongo.ReferenceField(Feeds)
     blocked = mongo.ListField(mongo.ObjectIdField())
  
# ===================================Community==========================================
class CommunityDetails(mongo.EmbeddedDocument):
     title = mongo.StringField()
     country = mongo.StringField(default="world")
     pp = mongo.URLField()
     
class Community(mongo.Document):
     field_id = mongo.ObjectIdField()
     details = mongo.EmbeddedDocumentField(CommunityDetails)
     members = mongo.ListField(field=mongo.ReferenceField(Users))
     posts = mongo.EmbeddedDocumentListField(ComPost)
 
class Field(mongo.Document):
     title = mongo.StringField(unique=True)
     communities = mongo.DictField(field=mongo.ReferenceField(Community))
# =============================================================================
