import json

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from listings.forms import AddListingForm, AddListingLocationForm, AddListingAmenityForm, MonthlyPriceFormSet, \
    EditListingForm, MonthlyPriceFormSetEdit, ListingFilterForm
from listings.models import Listing, Image, Amenity, Like


# Create your views here.
class ListingDetailsView(DetailView):
    model = Listing
    template_name = 'listings/listing-page.html'
    context_object_name = 'listing'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        listing = self.get_object()

        images = listing.images.all()
        mid_index = (len(images) + 1) // 2
        first_half_images = images[:mid_index]
        second_half_images = images[mid_index:]

        context["is_liked"] = False
        if self.request.user.is_authenticated:
            context["is_liked"] = listing.likes.filter(user=self.request.user).exists()
        context['first_half_images'] = first_half_images
        context['second_half_images'] = second_half_images
        return context


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
            listing.is_approved = False
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
    success_url = reverse_lazy('my-listings')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Listing.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.method == 'POST':
            context['location_form'] = kwargs.get('location_form', AddListingLocationForm(self.request.POST,
                                                                                          instance=self.object.location))
            context['monthly_price_formset_edit'] = kwargs.get('monthly_price_formset_edit',
                                                          MonthlyPriceFormSetEdit(self.request.POST, instance=self.object))
        else:
            context['location_form'] = AddListingLocationForm(instance=self.object.location)
            context['monthly_price_formset_edit'] = MonthlyPriceFormSetEdit(instance=self.object)

        context['images'] = self.object.images.all()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        location_form = AddListingLocationForm(request.POST, instance=self.object.location)
        monthly_price_formset_edit = MonthlyPriceFormSetEdit(request.POST, instance=self.object)

        if form.is_valid() and location_form.is_valid() and monthly_price_formset_edit.is_valid():
            location = location_form.save()
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.location = location
            listing.save()
            form.save_m2m()

            monthly_price_formset_edit.save()

            images = request.FILES.getlist('images')
            for img in images:
                Image.objects.create(listing=listing, image=img)

            return redirect(self.success_url)

        return self.render_to_response(
            self.get_context_data(
                form=form,
                location_form=location_form,
                monthly_price_formset=monthly_price_formset_edit
            )
        )


class DeleteListingView(LoginRequiredMixin, DeleteView):
    model = Listing
    template_name = 'listings/delete-listing-view.html'
    success_url = reverse_lazy('my-listings')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class DeleteImageView(LoginRequiredMixin, DeleteView):
    model = Image

    def get_success_url(self):
        listing_slug = self.object.listing.slug
        return reverse_lazy('edit-listing', kwargs={'slug': listing_slug})

    def get_queryset(self):
        return super().get_queryset().filter(listing__owner=self.request.user)


class UserListingsView(LoginRequiredMixin, ListView):
    model = Listing
    template_name = 'listings/user-listings.html'
    context_object_name = 'listings'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Listing.objects.filter(owner=self.request.user)


class ListingsByCategoryView(LoginRequiredMixin, ListView):
    model = Listing
    template_name = 'listings/listings-by-category.html'
    context_object_name = 'listings'

    def get_queryset(self):
        queryset = Listing.objects.filter(is_approved=True)

        listing_type = self.kwargs['listing_type']

        if listing_type != 'all':
            queryset = queryset.filter(type=listing_type)

        form = ListingFilterForm(self.request.GET or None)

        if form.is_valid():
            check_in = form.cleaned_data.get('check_in')
            check_out = form.cleaned_data.get('check_out')

            if check_in and check_out:
                queryset = queryset.exclude(
                    reservations__check_in__lt=check_out,
                    reservations__check_out__gt=check_in
                )

            if form.cleaned_data.get('name'):
                queryset = queryset.filter(title__icontains=form.cleaned_data['name'])

            if form.cleaned_data.get('max_people'):
                queryset = queryset.filter(max_people__gte=form.cleaned_data['max_people'])

            if form.cleaned_data.get('city'):
                queryset = queryset.filter(
                    Q(location__region__icontains=form.cleaned_data['city']) |
                    Q(location__city__icontains=form.cleaned_data['city'])
                )

            if form.cleaned_data.get('amenities'):
                for amenity in form.cleaned_data['amenities']:
                    queryset = queryset.filter(amenities=amenity)

            if form.cleaned_data.get('price_max'):
                queryset = queryset.filter(regular_price__lte=form.cleaned_data['price_max'])

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['amenities'] = Amenity.objects.all()
        context['form'] = ListingFilterForm(self.request.GET or None)
        context['listing_type'] = self.kwargs['listing_type']
        context['listing_locations'] = json.dumps([
            {
                'title': listing.title,
                'lat': listing.location.latitude,
                'lng': listing.location.longitude,
                'slug': listing.slug,
                'price': float(listing.regular_price),
                'image': listing.images.first().image.url if listing.images.exists() else ''
            }
            for listing in context['listings']
            if listing.location and listing.location.latitude and listing.location.longitude
        ])
        return context


def like(request: HttpRequest, listing_id: int):
    like_object = Like.objects.filter(to_listing_id=listing_id, user=request.user).first()

    if like_object:
        like_object.delete()
    else:
        Like.objects.create(
            to_listing_id=listing_id,
            user=request.user,
        )

    return redirect(request.META.get('HTTP_REFERER') + f"#{listing_id}")


class LikedListingsView(LoginRequiredMixin, ListView):
    model = Like
    template_name = 'listings/liked-listings.html'
    context_object_name = 'likes'

    def get_queryset(self):
        return Like.objects.filter(user=self.request.user).select_related("to_listing")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_likes = set(
            Like.objects.filter(user=self.request.user).values_list("to_listing_id", flat=True)
        )
        context["user_likes"] = user_likes
        return context

