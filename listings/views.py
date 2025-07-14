from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from listings.forms import AddListingForm, AddListingLocationForm, AddListingAmenityForm, MonthlyPriceFormSet, \
    EditListingForm
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
    success_url = reverse_lazy('my-listings') #TO MAKE TO RETURN TO DASHBOARD

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


class EditListingView(LoginRequiredMixin, UpdateView):
    model = Listing
    form_class = EditListingForm
    template_name = 'listings/edit-listing-page.html'
    success_url = reverse_lazy('my-listings')  # Или към dashboard

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.method == 'POST':
            context['location_form'] = kwargs.get('location_form', AddListingLocationForm(self.request.POST,
                                                                                          instance=self.object.location))
            context['monthly_price_formset'] = kwargs.get('monthly_price_formset',
                                                          MonthlyPriceFormSet(self.request.POST, instance=self.object))
        else:
            context['location_form'] = AddListingLocationForm(instance=self.object.location)
            context['monthly_price_formset'] = MonthlyPriceFormSet(instance=self.object)

        context['images'] = self.object.images.all()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        location_form = AddListingLocationForm(request.POST, instance=self.object.location)
        monthly_price_formset = MonthlyPriceFormSet(request.POST, instance=self.object)

        if form.is_valid() and location_form.is_valid() and monthly_price_formset.is_valid():
            location = location_form.save()
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.location = location
            listing.save()
            form.save_m2m()

            monthly_price_formset.save()

            images = request.FILES.getlist('images')
            for img in images:
                Image.objects.create(listing=listing, image=img)

            return redirect(self.success_url)

        return self.render_to_response(
            self.get_context_data(
                form=form,
                location_form=location_form,
                monthly_price_formset=monthly_price_formset
            )
        )


class DeleteListingView(LoginRequiredMixin, DeleteView):
    model = Listing
    template_name = 'listings/delete-listing-view.html'
    success_url = reverse_lazy('my-listings')

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class DeleteImageView(LoginRequiredMixin, DeleteView):
    model = Image

    def get_success_url(self):
        listing_id = self.object.listing.id
        return reverse_lazy('edit-listing', kwargs={'pk': listing_id})

    def get_queryset(self):
        return super().get_queryset().filter(listing__owner=self.request.user)


class UserListingsView(ListView):
    model = Listing
    template_name = 'listings/user-listings.html'
    context_object_name = 'listings'