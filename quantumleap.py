'''
Created on Jun 1, 2017

@author: Ahmad Nagib
'''
from handlers import (Handler, BlogHomepage, UserPosts, SignUp, Login,
                      Logout, Join, UserHomepage, NewPost, PostHandler,
                      LikePost, EditPost, EditComment, CommentOnPost,
                      DeletePost, DeleteComment)
import webapp2


app = webapp2.WSGIApplication([
    ('/blog/signup', SignUp),
    ('/blog/welcome', UserHomepage),
    ('/blog/login', Login),
    ('/blog/logout', Logout),
    ('/', BlogHomepage),
    ('/blog', BlogHomepage),
    ('/blog/newpost', NewPost),
    ('/blog/myposts', UserPosts),
    ('/blog/join', Join),
    ('/blog/comment-(\d+)', CommentOnPost),
    ('/blog/edit-(\d+)', EditPost),
    ('/blog/edit-comment-(\d+)', EditComment),
    ('/blog/like-(\d+)', LikePost),
    ('/blog/delete-(\d+)', DeletePost),
    ('/blog/delete-comment-(\d+)', DeleteComment),
    ('/blog/(\d+)', PostHandler),
], debug=True)
