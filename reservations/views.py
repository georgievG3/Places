from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from listings.models import Listing
from reservations.forms import ReservationForm


# Create your views here.
@login_required
def reserve_listing(request, slug):
    listing = get_object_or_404(Listing, slug=slug)

    if request.method == "POST":
        form = ReservationForm(request.POST, listing=listing)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.listing = listing
            reservation.save()
            return redirect('listing-detail', slug=slug)

    else:
        form = ReservationForm(listing=listing)

    return render(request, 'reservations/reservation.html', {
        'form': form,
        'listing': listing,
    })