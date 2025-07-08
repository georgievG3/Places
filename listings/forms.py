from django import forms

from listings.models import Listing


class AddListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        exclude = ('owner',)
