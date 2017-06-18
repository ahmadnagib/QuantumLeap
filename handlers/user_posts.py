from handler import Handler
from models import (SECRET, BlogPost, COMMENT, LIKE, USER)
from utils import (salt, hash_password, check_password, string_hash,
                   secure_cookie_value, check_cookie_integrity,
                   get_post_comments, get_likes_count, user_logged_in)


# handles the link to existing blog posts of signed-in-users
class UserPosts(Handler):

    def render_front(self, contents=""):
        self.render("blog.html", contents=contents)

    def get(self):

        if (self.user):
            signed_user = self.user
            contents = signed_user.blog_posts
            contents.order('-created_time')

            if contents.get():
                self.render_front(contents=contents)
            else:
                self.write("You have not added any posts yet!")

        else:
            self.redirect("/blog/login")
