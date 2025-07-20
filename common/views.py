from django.shortcuts import render
from django.views.generic import TemplateView

from listings.models import Listing


# Create your views here.

class IndexView(TemplateView):
    template_name = 'common/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['listings'] = Listing.objects.filter(is_approved = True)[:12]

        return context