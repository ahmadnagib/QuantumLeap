from handler import Handler
from models import (SECRET, BlogPost, COMMENT, LIKE, USER)
from utils import (salt, hash_password, check_password, string_hash,
                   secure_cookie_value, check_cookie_integrity,
                   get_post_comments, get_likes_count, user_logged_in,
                   post_exists, user_owns_post)


# handles the delete post link
class DeletePost(Handler):

    def render_front(self, post_id):
        self.render_front(post_id=post_id)

    @user_logged_in
    @post_exists
    @user_owns_post
    def get(self, post_id, blog_post, signed_username="", error=""):
        # capture the error when signed-in user is not the post's author
        if (error == 1):
            delete_error = 1
            self.redirect("/blog/%s?delete_error=%s" % (post_id, delete_error))

        else:
            blog_post.delete()
            self.redirect("/blog/welcome")
