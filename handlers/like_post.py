from handler import Handler
from models import (SECRET, BlogPost, COMMENT, LIKE, USER)
from utils import (salt, hash_password, check_password, string_hash,
                   secure_cookie_value, check_cookie_integrity,
                   get_post_comments, get_likes_count, post_exists,
                   user_logged_in)


# handles the like post link
class LikePost(Handler):

    def render_front(self, post_id):
        self.render_front(post_id=post_id)

    @user_logged_in
    @post_exists
    def get(self, post_id, blog_post):
        signed_user = self.user
        signed_username = self.user.username
        posting_username = blog_post.user.username

        # checks if the user already liked the post
        # fires an error if this is the case
        exisiting_like = signed_user.user_likes.filter('post =',
                                                       blog_post.key())
        if (exisiting_like.get()):
                like_error = 1
                self.redirect("/blog/%s?like_error=%s" % (post_id, like_error))

        # checks if the user is the post's author
        # fires an error if this is the case
        elif (signed_username == posting_username):
            like_error = 2
            self.redirect("/blog/%s?like_error=%s" % (post_id, like_error))

        # add a new like for this post
        else:
            new_like = LIKE(
                user=signed_user, post=blog_post)
            new_like.put()
            self.redirect("/blog/%s" % post_id)
