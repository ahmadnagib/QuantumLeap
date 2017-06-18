import webapp2
import jinja2
import os
from models import (SECRET, BlogPost, COMMENT, LIKE, USER)
from utils import (salt, hash_password, check_password, string_hash,
                   secure_cookie_value, check_cookie_integrity,
                   get_post_comments, get_likes_count)


template_directory = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                  'templates')
jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_directory),
    autoescape=True)


# used from udacity lessons
# handles rendering the right jinja template and the passed parameters
class Handler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **parameters):
        t = jinja_environment.get_template(template)
        return t.render(parameters)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def get_secure_cookie_value(self, cookie_name):
        cookie_value = self.request.cookies.get(cookie_name)
        return cookie_value and check_cookie_integrity(cookie_value)

    # inspired from udacity lessons after recommendation
    # by project reviewer, used mainly to check if there
    # is a logged-in user using "self.user"
    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        user_id = self.get_secure_cookie_value('user_id')
        self.user = user_id and USER.get_by_id(int(user_id))
