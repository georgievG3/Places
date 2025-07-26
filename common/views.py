from django.shortcuts import render
from django.views.generic import TemplateView, DetailView

from admin_panel.models import BlogPost
from listings.models import Listing


# Create your views here.

class IndexView(TemplateView):
    template_name = 'common/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['listings'] = Listing.objects.filter(is_approved = True)[:12]
        context['blog_posts'] = BlogPost.objects.all()[:12]

        return context


class BlogPostView(DetailView):
    model = BlogPost
    template_name = 'common/blog-post.html'
    context_object_name = 'blog_post'
