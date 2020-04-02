from classes import Users,UserDetails,Followers,Following
import mongoengine as mongo
import os

class Interface:
    def __init__(self):
        self.conn = mongo.connect(host = f"mongodb+srv://{os.environ['un']}:{os.environ['pw']}@cluster0-hlox9.mongodb.net/test?retryWrites=true&w=majority")
        self.user = False
        
    def register(self, un:str, email) -> bool:
         user = Users.objects(cognito_id=un)
         print("In register")
         if user:
             return False
         det = UserDetails(email=email,tags=[])
         user = Users(cognito_id=un, details = det,followers=Followers(),following=Following(),direct_chats=[],reporters_members=[],viewers=[],communities=[],profile_posts=[],blocked=[])
         user.save()
         return True
     
inf = Interface()

def lambda_handler(event, context):
    details = event["request"]["userAttributes"]
    user_id = details["sub"]
    email = details["email"]
    inf.register(user_id,email)