from models import (SECRET, BlogPost, COMMENT, LIKE, USER)
import hashlib
import random
import string
import hmac
from functools import wraps


# generate random string of 5 characters to be used in password hash
def salt():
    random_str = ''
    for i in range(5):
        random_str = random_str + random.choice(string.ascii_letters)
    return random_str


# uses username, password and salt to generate a password hash
def hash_password(username, password):
    random_str = salt()
    combination = username.encode(
        'utf-8') + password.encode('utf-8') + random_str.encode('utf-8')
    hashed_combination = hashlib.sha256(combination).hexdigest()
    return "%s,%s" % (hashed_combination, random_str)


# checks the stored hashed password against sign-in password
def check_password(username, password, hashed_combination):
    random_str = hashed_combination.split(',')[1]
    hashed_text = hashed_combination.split(',')[0]
    if (hashed_text == hashlib.sha256(
            username + password + random_str).hexdigest()):
        return True


# combines a secret string and user_id to generate a hash
def string_hash(user_id):
    return hmac.new(SECRET, user_id).hexdigest()


# generates the secure user_id cookie value including the hash
def secure_cookie_value(user_id):
    return "%s|%s" % (user_id, string_hash(user_id))


# checks the cookie user_id value against the hashed string
def check_cookie_integrity(cookie_value):
    if (isinstance(cookie_value, basestring)):
        value = cookie_value.split('|')[0]
        if cookie_value == secure_cookie_value(value):
            return value


# gets the comments made about a certain post
def get_post_comments(blog_post):
    post_comments = blog_post.post_comments
    post_comments.order('-created_time')
    if post_comments:
        return post_comments


# gets the number of likes for a certain post
def get_likes_count(blog_post):
    post_likes = blog_post.post_likes
    likes_count = 0
    for like in post_likes:
            likes_count += 1
    return likes_count


# check if there is a logged-user
# redirect to login page if no signed-in user
def user_logged_in(function):
    @wraps(function)
    def wrapper(self, post_id):
        if self.user:
            return function(self, post_id)
        else:
            self.redirect("/blog/login")
            return
    return wrapper


# inspired by the udacity project review
# checks if a passed blog_post exists when calling
# get or post methods
def post_exists(function):
    @wraps(function)
    def wrapper(self, post_id):
        blog_post = BlogPost.get_by_id(int(post_id))
        if blog_post:
            return function(self, post_id, blog_post=blog_post)
        else:
            self.write("Sorry, this blog post does not exists!")
            return
    return wrapper


# checks if a passed comment exists when calling
# get or post methods
def comment_exists(function):
    @wraps(function)
    def wrapper(self, comment_id):
        comment = COMMENT.get_by_id(int(comment_id))
        if comment:
            return function(self, comment_id, comment=comment)
        else:
            self.write("Sorry, this comment does not exists!")
            return
    return wrapper


# checks if the signed-in user is the post's author
# renders the edit post page in such case
# fires an error if the signed-in user is not the post's author
def user_owns_post(function):
    @wraps(function)
    def wrapper(self, post_id, blog_post=""):
        signed_username = self.user.username
        posting_user = blog_post.user.username
        if (signed_username == posting_user):
            return function(self, post_id=post_id,
                            blog_post=blog_post,
                            signed_username=signed_username)
        else:
            error = 1
            return function(self, post_id=post_id,
                            blog_post=blog_post, error=error)
    return wrapper


# checks if the signed-in user is the comment's author
# renders the edit comment page in such case
# fires an error if the signed-in user is not the post's author
def user_owns_comment(function):
    @wraps(function)
    def wrapper(self, comment_id, comment=""):
        signed_username = self.user.username
        commenting_user = comment.user.username
        post_id = comment.post.key().id()
        if (signed_username == commenting_user):
            return function(self, comment_id=comment_id, comment=comment,
                            signed_username=signed_username)
        else:
            error = 1
            return function(self, comment_id=comment_id,
                            comment=comment, error=error)
    return wrapper
