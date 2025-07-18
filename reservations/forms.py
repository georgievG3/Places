from django import forms
from django.core.exceptions import ValidationError

from reservations.models import Reservation


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['check_in', 'check_out', 'full_name', 'phone', 'note', 'guests']

        widgets = {
            'check_in': forms.TextInput(attrs={'readonly': 'readonly',}),
            'check_out': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

        labels = {
            'check_in': 'Настаняване:',
            'check_out': 'Напускане:',
            'guests': 'Брой гости:',
            'full_name': 'Име и фамилия:',
            'phone': 'Телефон:',
            'note': 'Бележки:',
        }


    def __init__(self, *args, **kwargs):
        self.listing = kwargs.pop('listing', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get("check_in")
        check_out = cleaned_data.get("check_out")
        guests = cleaned_data.get("guests")

        if check_in and check_out:
            if check_in > check_out:
                raise ValidationError("Датата на напускане трябва да е след датата на настаняване.")

            if self.listing and self.listing.reservations.filter(
                    check_in__lt=check_out,
                    check_out__gt=check_in
            ).exists():
                raise ValidationError("Тези дати вече са заети.")

        if guests and self.listing and guests > self.listing.max_people:
            raise ValidationError(f"Максималният брой гости за тази обява е {self.listing.max_people}.")

        return cleaned_data