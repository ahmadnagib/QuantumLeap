from google.appengine.ext import db
from user import USER
from blogpost import BlogPost


class LIKE(db.Model):
    user = db.ReferenceProperty(USER, collection_name='user_likes')
    post = db.ReferenceProperty(BlogPost, collection_name='post_likes')
    created_time = db.DateTimeProperty(auto_now_add=True)
