from handler import Handler
from models import (SECRET, BlogPost, COMMENT, LIKE, USER)
from utils import (salt, hash_password, check_password, string_hash,
                   secure_cookie_value, check_cookie_integrity,
                   get_post_comments, get_likes_count)


# handles the link to login page for signed-out-users
class Login(Handler):

    def render_front(self, username="", password="",
                     uname_error="", pass_error=""):
        self.render("login.html", username=username, password=password,
                    uname_error=uname_error, pass_error=pass_error)

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
            uname_error = ""
            pass_error = ""

            if (username == ""):
                uname_error = "Please enter a valid username!"

            if (password == ""):
                pass_error = "Please enter a valid password!"

            if (username and password):
                # checks for a user with a matching username in the data store
                q = USER.gql("WHERE username='%s'" % username)
                try:
                    stored_user = q.get()
                    stored_name = ""
                    stored_name = stored_user.username
                # fires an error if no matching username in datastore
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
