from handler import Handler
from models import (SECRET, BlogPost, COMMENT, LIKE, USER)
from utils import (salt, hash_password, check_password, string_hash,
                   secure_cookie_value, check_cookie_integrity,
                   get_post_comments, get_likes_count, post_exists,
                   user_logged_in, user_owns_post)


# handles the edit post link
class EditPost(Handler):

    def render_front(self, post_id, subject="", content="", error=""):
        self.render("editpost.html", post_id=post_id, subject=subject,
                    content=content, error=error)

    @user_logged_in
    @post_exists
    @user_owns_post
    def get(self, post_id="", blog_post="", signed_username="", error=""):
        # capture the error if the logged-in user is not the post's author
        if (error == 1):
            edit_error = 1
            self.redirect("/blog/%s?edit_error=%s" % (post_id, edit_error))

        else:
            subject = blog_post.subject
            content = blog_post.content
            self.render_front(
                    post_id=post_id,
                    subject=subject,
                    content=content)


    @user_logged_in
    @post_exists
    @user_owns_post
    def post(self, post_id="", blog_post="", signed_username="", error=""):
        if (error == 1):
            edit_error = 1
            self.redirect("/blog/%s?edit_error=%s" % (post_id, edit_error))

        else:
            subject = self.request.get("subject")
            content = self.request.get("content")
            # overwrite the stored post if both fields are filled-in
            if subject and content:
                blog_post.subject = subject
                blog_post.content = content
                blog_post.put()
                self.redirect("/blog/%s" % post_id)
            # fires an error if any of the fields are missing
            else:
                error = "we need both a subject and some blog post!"
                self.render_front(
                    post_id=post_id,
                    subject=subject,
                    content=content,
                    error=error)
