from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView

from listings.forms import AddListingForm, AddListingLocationForm, MonthlyPriceFormSet
from listings.models import Listing


# Create your views here.
class PendingListingsView(ListView):
    model = Listing
    context_object_name = 'pending_listings'
    template_name = 'admin_panel/pending_listings.html'

    def get_queryset(self):
        return Listing.objects.filter(is_approved=False)


class ReviewListingView(DetailView):
    model = Listing
    template_name = 'admin_panel/review-listing.html'
    context_object_name = 'listing'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['readonly'] = True
        context['form'] = AddListingForm(instance=self.object)
        context['location_form'] = AddListingLocationForm(instance=self.object.location)
        context['monthly_price_formset_edit'] = MonthlyPriceFormSet(instance=self.object)
        context['images'] = self.object.images.all()
        return context


class ApproveListingView(View):

    def post(self, request, slug):
        listing = Listing.objects.get(slug=slug)
        listing.is_approved = True
        listing.save()
        return redirect('index')

