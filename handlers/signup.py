from handler import Handler
from models import (SECRET, BlogPost, COMMENT, LIKE, USER)
from utils import (salt, hash_password, check_password, string_hash,
                   secure_cookie_value, check_cookie_integrity,
                   get_post_comments, get_likes_count)


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
        if self.user:
            self.redirect("/blog/welcome")

        else:
            self.render_front()

    def post(self):
        if self.user:
            self.redirect("/blog/welcome")

        else:
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
                q = USER.gql("WHERE username='%s'" % username)
                existing_user = q.get()
                try:
                    existing_name = existing_user.username
                    if (existing_name.lower() == username.lower()):
                        uname_error = "%s is already in use!" % username
                except AttributeError:
                    print "Could not find an existing username"

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
                    user = USER(
                        username=username, password=hashed_pass, email=email)

                else:
                    user = USER(
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
                                  uname_error=uname_error,
                                  pass_error=pass_error,
                                  vpass_error=vpass_error,
                                  email_error=email_error)
