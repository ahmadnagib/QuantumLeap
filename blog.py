'''
Created on Jun 1, 2017

@author: Ahmad Nagib
'''
from google.appengine.ext import db
import blog_tables
import os
import webapp2
import jinja2
import hashlib
import random
import string
import hmac
import time

template_directory = os.path.join(os.path.dirname(__file__), 'templates')
jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_directory),
    autoescape=True)


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
    return hmac.new(blog_tables.SECRET, user_id).hexdigest()


# generates the secure user_id cookie value including the hash
def secure_cookie_value(user_id):
    return "%s|%s" % (user_id, string_hash(user_id))


# checks the cookie user_id value against the hashed string
def check_cookie_integrity(cookie_value):
    if (isinstance(cookie_value, basestring)):
        value = cookie_value.split('|')[0]
        if cookie_value == secure_cookie_value(value):
            return value


# gets the signed-in user record using user_id cookie
def get_user_from_cookie(self):
    if check_cookie_integrity(self.request.cookies.get('user_id')):
        user_id_cookie = self.request.cookies.get('user_id')
        user_id = user_id_cookie.split('|')[0]
        user = blog_tables.USER.get_by_id(int(user_id))
        return user


# gets the username of the posting user
def get_user_from_post(self, post_id):
    return blog_tables.BlogPost.get_by_id(int(post_id)).posting_user


# gets the username of the commenting user
def get_user_from_comment(self, comment_id):
    return blog_tables.COMMENT.get_by_id(int(comment_id)).commenting_user


# gets the comments made about a certain post
def get_post_comments(post_id):
    q = blog_tables.COMMENT.gql(
        "WHERE post_id=%s ORDER BY created_time DESC" %
        int(post_id))
    if q:
        return q


# gets the number of likes for a certain post
def get_likes_count(post_id):
    likes = blog_tables.LIKE.gql("WHERE post_id=%s" % int(post_id))
    likes_count = 0
    if likes:
        for result in likes:
            likes_count += 1
        return likes_count


# used from udacity lessons
# handles rendering the right jinja template and the passed parameters
class Handler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **parameters):
        t = jinja_environment.get_template(template)
        return t.render(parameters)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


# handles the delete comment link
class DeleteComment(Handler):

    def render_front(self, comment_id):
        comment = blog_tables.COMMENT.get_by_id(int(comment_id))
        signed_user = get_user_from_cookie(self).username
        commenting_user = get_user_from_comment(self, comment_id=comment_id)
        post_id = comment.post_id

        # checks if the comment exists
        if not comment:
            self.write("Sorry, but this comment does not exist")
            return

        # checks if the signed-in user is the comment's author
        elif (signed_user == commenting_user):
            comment.delete()
            self.redirect("/blog/%s" % post_id)

        # fires an error as the signed-in user is not the comment's author
        else:
            delete_error = 2
            self.redirect("/blog/%s?delete_error=%s" % (post_id, delete_error))

    def get(self, comment_id):
        if check_cookie_integrity(self.request.cookies.get('user_id')):
            self.render_front(comment_id=comment_id)
        else:
            self.redirect("/blog/login")


# handles the delete post link
class DeletePost(Handler):

    def render_front(self, post_id):
        blog_post = blog_tables.BlogPost.get_by_id(int(post_id))
        signed_user = get_user_from_cookie(self).username
        posting_user = get_user_from_post(self, post_id=post_id)

        # checks if the post exists
        if not blog_post:
            self.write("Sorry, but this article does not exist")
            return

        # checks if the signed-in user is the post's author
        elif (signed_user == posting_user):
            blog_post.delete()
            self.redirect("/blog/welcome")

        # fires an error as the signed-in user is not the post's author
        else:
            delete_error = 1
            self.redirect("/blog/%s?delete_error=%s" % (post_id, delete_error))

    def get(self, post_id):
        if check_cookie_integrity(self.request.cookies.get('user_id')):
            self.render_front(post_id=post_id)
        else:
            self.redirect("/blog/login")


# handles the comment on post link
class CommentOnPost(Handler):

    def render_front(
            self,
            post_id,
            blog_post,
            subject="",
            content="",
            error=""):
        self.render(
            "add-comment.html",
            post_id=post_id,
            blog_post=blog_post,
            subject=subject,
            content=content,
            error=error)

    def get(self, post_id):
        # checks if there is a signed-in user
        if check_cookie_integrity(self.request.cookies.get('user_id')):
            blog_post = blog_tables.BlogPost.get_by_id(int(post_id))
            signed_user = get_user_from_cookie(self).username
            self.render_front(post_id=post_id, blog_post=blog_post)

        # direct to login page if no signed-in users
        else:
            self.redirect("/blog/login")

    def post(self, post_id):
        subject = self.request.get("subject")
        content = self.request.get("content")

        # checks if the fields are all filled-in
        if subject and content:
            commenting_user = get_user_from_cookie(self).username
            new_comment = blog_tables.COMMENT(
                commenting_user=commenting_user,
                post_id=int(post_id),
                subject=subject,
                content=content)
            new_comment.put()
            self.redirect("/blog/%s" % post_id)

        # fires an error as one or more fields are empty
        else:
            blog_post = blog_tables.BlogPost.get_by_id(int(post_id))
            error = "we need both a title and some comment!"
            self.render_front(
                post_id=post_id,
                blog_post=blog_post,
                subject=subject,
                content=content,
                error=error)


# handles the edit comment link
class EditComment(Handler):

    def render_front(
            self,
            post_id,
            comment_id,
            subject="",
            content="",
            error=""):
        self.render(
            "editcomment.html",
            post_id=post_id,
            comment_id=comment_id,
            subject=subject,
            content=content,
            error=error)

    def get(self, comment_id):
        if check_cookie_integrity(self.request.cookies.get('user_id')):
            comment = blog_tables.COMMENT.get_by_id(int(comment_id))
            signed_user = get_user_from_cookie(self).username
            commenting_user = get_user_from_comment(
                self, comment_id=comment_id)
            subject = comment.subject
            content = comment.content
            post_id = int(comment.post_id)

            # checks if the signed-in user is the comment's author
            # renders the edit comment page in such case
            if (signed_user == commenting_user):
                self.render_front(
                    post_id=post_id,
                    comment_id=comment_id,
                    subject=subject,
                    content=content)
            # fires an error as the signed-in user is not the comment's author
            else:
                edit_error = 2
                self.redirect("/blog/%s?edit_error=%s" % (post_id, edit_error))
        # redirect to login page if no signed-in user
        else:
            self.redirect("/blog/login")

    def post(self, comment_id):
        subject = self.request.get("subject")
        content = self.request.get("content")
        posting_user = get_user_from_cookie(self).username
        comment = blog_tables.COMMENT.get_by_id(int(comment_id))
        post_id = comment.post_id
        # overwrite the stored comment if both fields are filled-in
        if subject and content:
            comment.subject = subject
            comment.content = content
            comment.put()
            self.redirect("/blog/%s" % post_id)
        # fires an error if any of the fields are missing
        else:
            error = "we need both a subject and some comment!"
            self.render_front(
                post_id=post_id,
                comment_id=comment_id,
                subject=subject,
                content=content,
                error=error)


# handles the edit post link
class EditPost(Handler):

    def render_front(self, post_id, subject="", content="", error=""):
        self.render("editpost.html", post_id=post_id, subject=subject,
                    content=content, error=error)

    def get(self, post_id):
        if check_cookie_integrity(self.request.cookies.get('user_id')):
            blog_post = blog_tables.BlogPost.get_by_id(int(post_id))
            signed_user = get_user_from_cookie(self).username
            posting_user = get_user_from_post(self, post_id=post_id)
            subject = blog_post.subject
            content = blog_post.content

            # checks if the signed-in user is the post's author
            # renders the edit post page in such case
            if (signed_user == posting_user):
                self.render_front(
                    post_id=post_id,
                    subject=subject,
                    content=content)

            # fires an error as the signed-in user is not the post's author
            else:
                edit_error = 1
                self.redirect("/blog/%s?edit_error=%s" % (post_id, edit_error))
        # redirect to login page if no signed-in user
        else:
            self.redirect("/blog/login")

    def post(self, post_id):
        subject = self.request.get("subject")
        content = self.request.get("content")
        # overwrite the stored post if both fields are filled-in
        if subject and content:
            posting_user = get_user_from_cookie(self).username
            blog_post = blog_tables.BlogPost.get_by_id(int(post_id))
            blog_post.subject = subject
            blog_post.content = content
            blog_post.put()
            self.redirect("/blog/%s" % post_id)
        # fires an error if any of the fields are missing
        else:
            error = "we need both a subject and some blog post!"
            self.render_front(
                post_id=post_id,
                subject=subject,
                content=content,
                error=error)


# handles the like post link
class LikePost(Handler):

    def render_front(self, post_id):
        blog_post = blog_tables.BlogPost.get_by_id(int(post_id))
        signed_user_id = get_user_from_cookie(self).key().id()
        signed_user = get_user_from_cookie(self).username
        posting_user = get_user_from_post(self, post_id=post_id)
        # checks if the user already liked the post
        # fires an error if this is the case
        try:
            query = blog_tables.LIKE.gql(
                "WHERE user_id=%s AND post_id=%s" %
                (int(signed_user_id), int(post_id)))
            liked = query.get().key().id()
            like_error = 1
            self.redirect("/blog/%s?like_error=%s" % (post_id, like_error))

        except AttributeError:
            # checks if the user is the post's author
            # fires an error if this is the case
            if (signed_user == posting_user):
                like_error = 2
                self.redirect("/blog/%s?like_error=%s" % (post_id, like_error))
            # add a new like for this post
            else:
                new_like = blog_tables.LIKE(
                    user_id=signed_user_id, post_id=int(post_id))
                new_like.put()
                self.redirect("/blog/%s" % post_id)

    def get(self, post_id):
        if check_cookie_integrity(self.request.cookies.get('user_id')):
            self.render_front(post_id=post_id)
        else:
            self.redirect("/blog/login")


# handles individual blog post pages
class PostHandler(Handler):

    def render_front(self, post_id):
        blog_post = blog_tables.BlogPost.get_by_id(int(post_id))
        likes_count = get_likes_count(int(post_id))
        like_error = 0
        delete_error = 0
        edit_error = 0
        comments = get_post_comments(int(post_id))

        if not blog_post:
            self.write("Sorry, but this page does not exist")
            return
        # capture error id passed in the url
        if (self.request.get('like_error')):
            like_error = int(self.request.get('like_error'))

        elif (self.request.get('edit_error')):
            edit_error = int(self.request.get('edit_error'))

        elif (self.request.get('delete_error')):
            delete_error = int(self.request.get('delete_error'))

        self.render(
            "article.html",
            blog_post=blog_post,
            likes_count=likes_count,
            comments=comments,
            like_error=like_error,
            delete_error=delete_error,
            edit_error=edit_error)

    def get(self, post_id):
        self.render_front(post_id=post_id)


# handles adding a new blog post
class NewPost(Handler):

    def render_front(self, subject="", content="", error=""):
        self.render("newpost.html", subject=subject,
                    content=content, error=error)

    def get(self):
        # redirects to join blog page if no user is logged-in
        if check_cookie_integrity(self.request.cookies.get('user_id')):
            self.render_front()
        else:
            self.redirect("/blog/join")

    def post(self):
        subject = self.request.get("subject")
        content = self.request.get("content")
        # adds a new post to the datastore if both fields are filled-in
        if subject and content:
            posting_user = get_user_from_cookie(self).username
            new_post = blog_tables.BlogPost(
                subject=subject, content=content, posting_user=posting_user)
            new_post.put()
            post_id = new_post.key().id()
            self.redirect("/blog/%s" % post_id)
        # fires an error message if any of the fields is missing
        else:
            error = "we need both a subject and some blog post!"
            self.render_front(subject=subject, content=content, error=error)


# handles the link to homepage for signed-in-users
class UserHomepage(Handler):

    def get(self):
        if get_user_from_cookie(self):
            self.render(
                "welcome.html",
                username=get_user_from_cookie(self).username)
        else:
            self.redirect("/blog/join")


# handles the link to join the blog for signed-out-users
class Join(Handler):

    def render_front(self):
        self.render("join.html")

    def get(self):
        if check_cookie_integrity(self.request.cookies.get('user_id')):
            self.redirect("/blog/welcome")
        else:
            self.render_front()


# handles the link to logout for signed-in-users
class Logout(Handler):

    def get(self):
        if (self.request.cookies.get('user_id')):
            self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')
        self.redirect("/blog/login")


# handles the link to login page for signed-out-users
class Login(Handler):

    def render_front(self, username="", password="",
                     uname_error="", pass_error=""):
        self.render("login.html", username=username, password=password,
                    uname_error=uname_error, pass_error=pass_error)

    def get(self):
        if check_cookie_integrity(self.request.cookies.get('user_id')):
            self.redirect("/blog/welcome")

        else:
            self.render_front()

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        uname_error = ""
        pass_error = ""

        if (username == ""):
            uname_error = "Please enter a valid username!"

        if (password == ""):
            pass_error = "Please enter a valid password!"

        if (username and password):
            # checks for a user with a matching username in the data store
            q = blog_tables.USER.gql("WHERE username='%s'" % username)
            stored_user = q.get()
            stored_name = ""
            try:
                stored_name = stored_user.username
            # fires an error if no matching username in data store
            except AttributeError:
                uname_error = "This username does not exist"
                self.render_front(
                    username=username,
                    password=password,
                    uname_error=uname_error,
                    pass_error=pass_error)
                print "Something went wrong with the database query"

            if (stored_name != ""):
                # checks the entered password against the stored one
                # update the user_id cookie value if passwords match
                stored_password = stored_user.password
                if check_password(username, password, stored_password):
                    stored_user_id = stored_user.key().id()
                    self.response.headers.add_header(
                        'Set-Cookie', 'user_id=%s; Path=/' %
                        secure_cookie_value(
                            str(stored_user_id)))
                    self.redirect("/blog/welcome")
                else:
                    pass_error = """The entered password does not match
                                    the stored password"""

                self.render_front(
                    username=username,
                    password=password,
                    uname_error=uname_error,
                    pass_error=pass_error)

        else:
            self.render_front(
                username=username,
                password=password,
                uname_error=uname_error,
                pass_error=pass_error)


# handles the link to sigup page for signed-out-users
class SignUp(Handler):

    def render_front(self, username="", password="", verify="",
                     email="", uname_error="", pass_error="",
                     vpass_error="", email_error=""):
        self.render("registration.html", username=username, password=password,
                    verify=verify, email=email, uname_error=uname_error,
                    pass_error=pass_error, vpass_error=vpass_error,
                    email_error=email_error)

    def get(self):
        if check_cookie_integrity(self.request.cookies.get('user_id')):
            self.redirect("/blog/welcome")

        else:
            self.render_front()

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")
        uname_error = ""
        pass_error = ""
        vpass_error = ""
        email_error = ""
        # checks if the entered username already exists
        if username:
            q = blog_tables.USER.gql("WHERE username='%s'" % username)
            existing_user = q.get()
            try:
                existing_name = existing_user.username
                if (existing_name.lower() == username.lower()):
                    uname_error = "%s is already in use!" % username
            except AttributeError:
                print "Oops!  That was no valid number.  Try again..."

        # checks if any of the entries is absent
        elif (username == ""):
            uname_error = "Please enter a valid username!"

        if (password == ""):
            pass_error = "Please enter a valid password!"

        if (verify == ""):
            vpass_error += "Please enter a valid verification!"

        # checks if the password does not match its verification
        if (password != verify):
            vpass_error += "The password did not match its verification"
        # if no errors hash the password and adde a new user record
        if (uname_error == "" and pass_error == "" and vpass_error == ""):
            hashed_pass = hash_password(username, password)

            if email:
                user = blog_tables.USER(
                    username=username, password=hashed_pass, email=email)

            else:
                user = blog_tables.USER(
                    username=username, password=hashed_pass)

            user.put()
            user_id = user.key().id()
            self.response.headers.add_header(
                'Set-Cookie', 'user_id=%s; Path=/' %
                secure_cookie_value(
                    str(user_id)))
            self.redirect("/blog/welcome")

        else:
            self.render_front(username=username, password=password,
                              verify=verify, email=email,
                              uname_error=uname_error, pass_error=pass_error,
                              vpass_error=vpass_error, email_error=email_error)


# handles the link to existing blog posts of signed-in-users
class UserPosts(Handler):

    def render_front(self, contents=""):
        posting_user = get_user_from_cookie(self).username
        contents = blog_tables.BlogPost.gql(
            "WHERE posting_user='%s' ORDER BY created_time" %
            posting_user)
        self.render("blog.html", contents=contents)

    def get(self):
        self.render_front()


# handles the link to blog home page
# updated with the latest 10 blog posts
class BlogHomepage(Handler):

    def render_front(self, contents=""):
        contents = blog_tables.BlogPost.gql(
            "ORDER BY created_time DESC LIMIT 10;")
        self.render("blog.html", contents=contents)

    def get(self):
        self.render_front()


app = webapp2.WSGIApplication([
    ('/blog/signup', SignUp),
    ('/blog/welcome', UserHomepage),
    ('/blog/login', Login),
    ('/blog/logout', Logout),
    ('/', BlogHomepage),
    ('/blog', BlogHomepage),
    ('/blog/newpost', NewPost),
    ('/blog/myposts', UserPosts),
    ('/blog/join', Join),
    ('/blog/comment-(\d+)', CommentOnPost),
    ('/blog/edit-(\d+)', EditPost),
    ('/blog/edit-comment-(\d+)', EditComment),
    ('/blog/like-(\d+)', LikePost),
    ('/blog/delete-(\d+)', DeletePost),
    ('/blog/delete-comment-(\d+)', DeleteComment),
    ('/blog/(\d+)', PostHandler),
], debug=True)
