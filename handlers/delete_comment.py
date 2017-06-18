from handler import Handler
from models import (SECRET, BlogPost, COMMENT, LIKE, USER)
from utils import (salt, hash_password, check_password, string_hash,
                   secure_cookie_value, check_cookie_integrity,
                   get_post_comments, get_likes_count, comment_exists,
                   user_logged_in, user_owns_comment)


# handles the delete comment link
class DeleteComment(Handler):

    def render_front(self, comment_id):
        self.render_front(comment_id=comment_id)

    @user_logged_in
    @comment_exists
    @user_owns_comment
    def get(self, comment_id, comment, signed_username="", error=""):
        post_id = comment.post.key().id()
        # capture the error when signed-in user is not the comment's author
        if (error == 1):
            delete_error = 2
            self.redirect("/blog/%s?delete_error=%s" % (post_id, delete_error))

        else:
            comment.delete()
            self.redirect("/blog/%s" % post_id)
