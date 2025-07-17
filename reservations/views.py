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