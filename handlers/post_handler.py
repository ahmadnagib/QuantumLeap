from handler import Handler
from models import (SECRET, BlogPost, COMMENT, LIKE, USER)
from utils import (salt, hash_password, check_password, string_hash,
                   secure_cookie_value, check_cookie_integrity,
                   get_post_comments, get_likes_count, post_exists)


# handles individual blog post pages
class PostHandler(Handler):

    def render_front(self, blog_post="",
                     likes_count="",
                     comments="",
                     like_error="",
                     delete_error="",
                     edit_error=""):

        self.render(
            "article.html",
            blog_post=blog_post,
            likes_count=likes_count,
            comments=comments,
            like_error=like_error,
            delete_error=delete_error,
            edit_error=edit_error)

    @post_exists
    def get(self, post_id, blog_post):
        likes_count = get_likes_count(blog_post)
        comments = get_post_comments(blog_post)
        like_error = 0
        delete_error = 0
        edit_error = 0

        # capture error id passed in the url
        if (self.request.get('like_error')):
            like_error = int(self.request.get('like_error'))

        elif (self.request.get('edit_error')):
            edit_error = int(self.request.get('edit_error'))

        elif (self.request.get('delete_error')):
            delete_error = int(self.request.get('delete_error'))

        self.render_front(blog_post=blog_post,
                          likes_count=likes_count,
                          comments=comments,
                          like_error=like_error,
                          delete_error=delete_error,
                          edit_error=edit_error)
