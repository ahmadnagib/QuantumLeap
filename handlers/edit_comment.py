from handler import Handler
from models import (SECRET, BlogPost, COMMENT, LIKE, USER)
from utils import (salt, hash_password, check_password, string_hash,
                   secure_cookie_value, check_cookie_integrity,
                   get_post_comments, get_likes_count, user_logged_in,
                   comment_exists, user_owns_comment)


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

    @user_logged_in
    @comment_exists
    @user_owns_comment
    def get(self, comment_id, comment, signed_username="", error=""):
        post_id = comment.post.key().id()
        # capture the error that signed-in user is not the comment's author
        if (error == 1):
            edit_error = 2
            self.redirect("/blog/%s?edit_error=%s" % (post_id, edit_error))

        else:
            subject = comment.subject
            content = comment.content
            self.render_front(
                    post_id=post_id,
                    comment_id=comment_id,
                    subject=subject,
                    content=content)

    @user_logged_in
    @comment_exists
    @user_owns_comment
    def post(self, comment_id, comment, signed_username="", error=""):
        if (error == 1):
            edit_error = 2
            self.redirect("/blog/%s?edit_error=%s" % (post_id, edit_error))

        else:
            post_id = comment.post.key().id()
            subject = self.request.get("subject")
            content = self.request.get("content")
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
