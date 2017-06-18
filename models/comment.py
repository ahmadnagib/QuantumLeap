from google.appengine.ext import db
from user import USER
from blogpost import BlogPost


class COMMENT(db.Model):
    user = db.ReferenceProperty(USER, collection_name='user_comments')
    post = db.ReferenceProperty(BlogPost, collection_name='post_comments')
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created_time = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
