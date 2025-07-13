from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView

from listings.forms import AddListingForm, AddListingLocationForm, AddListingAmenityForm, MonthlyPriceFormSet
from listings.models import Listing, Image


# Create your views here.
class ListingDetailsView(DetailView):
    model = Listing
    template_name = 'listings/listing-page.html'
    context_object_name = 'listing'


class AddListingView(LoginRequiredMixin, CreateView):
    model = Listing
    form_class = AddListingForm
    template_name = 'listings/add-listing-page.html'
    success_url = reverse_lazy('index') #TO MAKE TO RETURN TO DASHBOARD

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['location_form'] = kwargs.get('location_form', AddListingLocationForm())
        context['monthly_price_formset'] = kwargs.get('monthly_price_formset', MonthlyPriceFormSet())

        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        location_form = AddListingLocationForm(request.POST)
        monthly_price_formset = MonthlyPriceFormSet(request.POST)

        if form.is_valid() and location_form.is_valid() and monthly_price_formset.is_valid():
            location = location_form.save()
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.location = location
            listing.save()
            form.save_m2m()

            monthly_price_formset.instance = listing
            monthly_price_formset.save()

            images = request.FILES.getlist('images')
            for img in images:
                Image.objects.create(listing=listing, image=img)

            return self.form_valid(form)

        self.object = None
        return self.render_to_response(
            self.get_context_data(
                form=form,
                location_form=location_form,
                monthly_price_formset=monthly_price_formset
            )
        )


class UserListingsView(ListView):
    model = Listing
    template_name = 'listings/user-listings.html'
    context_object_name = 'listings'