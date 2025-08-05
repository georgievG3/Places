from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView

from listings.models import Listing
from reservations.forms import ReservationForm
from reservations.models import Reservation


# Create your views here.
@login_required
def reserve_listing_view(request, slug):
    listing = get_object_or_404(Listing, slug=slug)
    check_in = None
    check_out = None

    if request.method == "POST":
        form = ReservationForm(request.POST, listing=listing)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.listing = listing
            reservation.save()
            return redirect('listing-detail', slug=slug)
    else:
        check_in = request.GET.get('check_in')
        check_out = request.GET.get('check_out')

        initial_data = {}
        if check_in and check_out:
            initial_data = {'check_in': check_in, 'check_out': check_out}

        form = ReservationForm(initial=initial_data, listing=listing)

    return render(request, 'reservations/reservation.html', {
        'form': form,
        'listing': listing,
        'prefilled_check_in': check_in,
        'prefilled_check_out': check_out,
    })


class UserReservationsView(ListView):
    model = Reservation
    template_name = 'reservations/user-reservations.html'
    context_object_name = 'reservations'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)


class UserReservationDeleteView(LoginRequiredMixin, DeleteView):
    model = Reservation
    template_name = 'reservations/delete-reservation.html'
    success_url = reverse_lazy('my_reservations')
    slug_field = 'pk'
    slug_url_kwarg = 'pk'
    context_object_name = 'reservation'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)