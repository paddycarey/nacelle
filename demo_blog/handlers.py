# third-party imports
from google.appengine.ext import ndb

# local imports
from demo_blog.models import Post
from nacelle.handlers.base import TemplateHandler


class BlogHandler(TemplateHandler):

    def get(self, post_id=None):

        if post_id is None:
            return self.render_blog()
        else:
            return self.render_post(post_id)

    def render_blog(self):

        # do async query early so we can pull posts as needed as we're rendering our template
        posts = Post.query().filter(Post.published == True).order(-Post.creation_time).iter(keys_only=True)
        posts = ndb.get_multi_async(posts)

        # render template and return
        template = 'demo_blog/index.html'
        return self.render_response(template, {'posts': posts})

    def render_post(self, post_id):

        post = Post.get_by_id(post_id)
        if post is None:
            return self.abort(404)

        # render template and return
        template = 'demo_blog/post.html'
        return self.render_response(template, {'post': post})
