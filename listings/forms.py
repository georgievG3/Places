from django import forms

from listings.models import Listing, Location, Amenity, Image


class AddListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        exclude = ('owner', 'location',)

        widgets = {
            'amenities': forms.CheckboxSelectMultiple(),
            'description': forms.Textarea(attrs={'style': 'resize: none'}),
        }

        labels = {
            'type': 'Вид на мястото',
            'title': 'Име',
            'camping': 'Къмпинг',
            'rooms': 'Брой стаи',
            'min_nights': 'Минималнен брой нощувки',
            'square_meters': 'Квадратни метри',
            'pets_allowed': 'Разрешено за животни',
            'mini_description': 'Малко описание',
        }


class AddListingLocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = '__all__'

        labels = {
            'name': 'Име',
            'region': 'Държава',
            'address': 'Адрес',
            'terrain_type': 'Вид на терена',
        }

        widgets = {
            'latitude': forms.HiddenInput(attrs={'id': 'id_latitude'}),
            'longitude': forms.HiddenInput(attrs={'id': 'id_longitude'}),
        }


class AddListingAmenityForm(forms.ModelForm):
    class Meta:
        model = Amenity
        fields = '__all__'


class AddListingImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image', )

