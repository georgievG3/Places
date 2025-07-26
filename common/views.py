from django.shortcuts import render
from django.views.generic import TemplateView, DetailView

from admin_panel.models import BlogPost
from listings.models import Listing


# Create your views here.

class IndexView(TemplateView):
    template_name = 'common/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        listings = Listing.objects.filter(is_approved=True).select_related("location")

        markers = []
        for listing in listings:
            if listing.location and listing.location.latitude and listing.location.longitude:
                markers.append({
                    'title': listing.title,
                    'lat': listing.location.latitude,
                    'lng': listing.location.longitude,
                    'slug': listing.slug,
                    'price': float(listing.regular_price),
                    'image': listing.images.first().image.url if listing.images.exists() else ''
                })

        context['listings'] = listings[:12]
        context['markers'] = markers
        context['blog_posts'] = BlogPost.objects.all()[:12]
        return context


class BlogPostView(DetailView):
    model = BlogPost
    template_name = 'common/blog-post.html'
    context_object_name = 'blog_post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['other_blog_posts'] = BlogPost.objects.all()[:2]

        return context
