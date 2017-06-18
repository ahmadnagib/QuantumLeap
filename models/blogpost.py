from google.appengine.ext import db
from user import USER


class BlogPost(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    user = db.ReferenceProperty(USER, collection_name='blog_posts')
    created_time = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
