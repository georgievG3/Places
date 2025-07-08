from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from listings.forms import AddListingForm
from listings.models import Listing

# Create your views here.
def listing_page_view(request):
    return render(request, 'listings/listing-page.html')


class AddListingView(LoginRequiredMixin, CreateView):
    model = Listing
    form_class = AddListingForm
    template_name = 'listings/add-listing-page.html'
    success_url = reverse_lazy('index') #TO MAKE TO RETURN TO DASHBOARD

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)

