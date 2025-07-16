from django import forms
from django.core.exceptions import ValidationError

from reservations.models import Reservation


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['check_in', 'check_out', 'full_name', 'phone', 'note']


    def __init__(self, *args, **kwargs):
        self.listing = kwargs.pop('listing', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get("check_in")
        check_out = cleaned_data.get("check_out")

        if check_in and check_out:
            if check_in > check_out:
                raise ValidationError("Датата на напускане трябва да е след датата на настаняване.")

            if self.listing and self.listing.reservations.filter(
                    check_in__lt=check_out,
                    check_out__gt=check_in
            ).exists():
                raise ValidationError("Тези дати вече са заети.")

        return cleaned_data