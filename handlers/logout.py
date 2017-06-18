from handler import Handler
from models import (SECRET, BlogPost, COMMENT, LIKE, USER)
from utils import (salt, hash_password, check_password, string_hash,
                   secure_cookie_value, check_cookie_integrity,
                   get_post_comments, get_likes_count)


# handles the link to logout for signed-in-users
class Logout(Handler):

    def get(self):
        if self.user:
            self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

        self.redirect("/blog/login")
