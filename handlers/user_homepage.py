from handler import Handler
from models import (SECRET, BlogPost, COMMENT, LIKE, USER)
from utils import (salt, hash_password, check_password, string_hash,
                   secure_cookie_value, check_cookie_integrity,
                   get_post_comments, get_likes_count)


# handles the link to homepage for signed-in-users
class UserHomepage(Handler):

    def get(self):
        if self.user:
            self.render(
                "welcome.html",
                username=self.user.username)
        else:
            self.redirect("/blog/join")
