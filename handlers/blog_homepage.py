from handler import Handler
from models import (SECRET, BlogPost, COMMENT, LIKE, USER)
from utils import (salt, hash_password, check_password, string_hash,
                   secure_cookie_value, check_cookie_integrity,
                   get_post_comments, get_likes_count)


# handles the link to blog home page
# updated with the latest 10 blog posts
class BlogHomepage(Handler):

    def render_front(self, contents=""):
        self.render("blog.html", contents=contents)

    def get(self):
    	# get the latest 10 blog posts
        contents = BlogPost.gql(
            "ORDER BY created_time DESC LIMIT 10;")
        self.render_front(contents=contents)
