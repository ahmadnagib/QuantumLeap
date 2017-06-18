from handler import Handler
from models import (SECRET, BlogPost, COMMENT, LIKE, USER)
from utils import (salt, hash_password, check_password, string_hash,
                   secure_cookie_value, check_cookie_integrity,
                   get_post_comments, get_likes_count)


# handles the link to join the blog for signed-out-users
class Join(Handler):

    def render_front(self):
        self.render("join.html")

    def get(self):
        if self.user:
            self.redirect("/blog/welcome")
        else:
            self.render_front()
