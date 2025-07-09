from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from listings.forms import AddListingForm, AddListingLocationForm, AddListingAmenityForm, AddListingImageForm
from listings.models import Listing

# Create your views here.
def listing_page_view(request):
    return render(request, 'listings/listing-page.html')


class AddListingView(LoginRequiredMixin, CreateView):
    model = Listing
    form_class = AddListingForm
    template_name = 'listings/add-listing-page.html'
    success_url = reverse_lazy('index') #TO MAKE TO RETURN TO DASHBOARD

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['location_form'] = kwargs.get('location_form', AddListingLocationForm())
        context['image_form'] = kwargs.get('image_form', AddListingImageForm())

        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        location_form = AddListingLocationForm(request.POST)
        image_form = AddListingImageForm(request.POST, request.FILES)

        if form.is_valid() and location_form.is_valid() and image_form.is_valid():
            location = location_form.save()
            image = image_form.save()

            listing = form.save(commit=False)
            listing.owner = request.user
            listing.location = location
            image.listing = listing
            image.save()
            listing.save()
            form.save_m2m()
            return self.form_valid(form)

        self.object = None
        return self.render_to_response(
            self.get_context_data(form=form, location_form=location_form, image_form=image_form)
        )


