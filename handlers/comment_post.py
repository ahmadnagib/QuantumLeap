from handler import Handler
from models import (SECRET, BlogPost, COMMENT, LIKE, USER)
from utils import (salt, hash_password, check_password, string_hash,
                   secure_cookie_value, check_cookie_integrity,
                   get_post_comments, get_likes_count, user_logged_in,
                   post_exists)


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

    @user_logged_in
    @post_exists
    def get(self, post_id, blog_post):
        self.render_front(post_id=post_id, blog_post=blog_post)

    @user_logged_in
    @post_exists
    def post(self, post_id, blog_post):
        signed_user = self.user
        subject = self.request.get("subject")
        content = self.request.get("content")

        # checks if the fields are all filled-in
        if subject and content:
            new_comment = COMMENT(
                user=signed_user,
                post=blog_post,
                subject=subject,
                content=content)
            new_comment.put()
            self.redirect("/blog/%s" % post_id)

        # fires an error as one or more fields are empty
        else:
            error = "we need both a title and some comment!"
            self.render_front(
                post_id=post_id,
                blog_post=blog_post,
                subject=subject,
                content=content,
                error=error)
