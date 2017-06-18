from handler import Handler
from models import (SECRET, BlogPost, COMMENT, LIKE, USER)
from utils import (salt, hash_password, check_password, string_hash,
                   secure_cookie_value, check_cookie_integrity,
                   get_post_comments, get_likes_count, user_logged_in)


# handles adding a new blog post
class NewPost(Handler):

    def render_front(self, subject="", content="", error=""):
        self.render("newpost.html", subject=subject,
                    content=content, error=error)

    def get(self):
        if self.user:
            self.render_front()

        else:
            self.redirect("/blog/login")

    def post(self):
        if self.user:

            subject = self.request.get("subject")
            content = self.request.get("content")
            # adds a new post to the datastore if both fields are filled-in
            if subject and content:
                posting_user = self.user
                new_post = BlogPost(
                    subject=subject, content=content, user=posting_user)
                new_post.put()
                post_id = new_post.key().id()
                self.redirect("/blog/%s" % post_id)
            # fires an error message if any of the fields is missing
            else:
                error = "we need both a subject and some blog post!"
                self.render_front(subject=subject, content=content,
                                  error=error)

        else:
            self.redirect("/blog/login")
