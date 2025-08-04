from django import forms
from django.forms import inlineformset_factory

from listings.models import Listing, Location, Amenity, Image, MonthlyPrice, Comment


class AddListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        exclude = ('owner', 'location', 'slug', 'is_approved')

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
            'max_people': 'Максимален брой хора',
            'square_meters': 'Квадратни метри',
            'pets_allowed': 'Разрешено за животни',
            'mini_description': 'Малко описание',
            'regular_price': 'Редовна цена',
        }


class AddListingLocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = '__all__'

        labels = {
            'name': 'Име',
            'region': 'Държава',
            'address': 'Адрес',
            'city': 'Град',
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


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']

ImageFormSet = inlineformset_factory(
    Listing,
    Image,
    form=ImageForm,
    extra=1,
    min_num=5,
    validate_min=True,
    can_delete=True
)

ImageFormSetEdit = inlineformset_factory(
    Listing,
    Image,
    form=ImageForm,
    extra=1,
    can_delete=True,
    validate_min=False,
    min_num=0,
)


class MonthlyPriceForm(forms.ModelForm):
    class Meta:
        model = MonthlyPrice
        fields = ['month', 'price']
        labels = {
            'month': 'Месец',
            'price': 'Цена за месеца',
        }


MonthlyPriceFormSet = inlineformset_factory(
    Listing,
    MonthlyPrice,
    form=MonthlyPriceForm,
    fields=['month', 'price'],
    extra=5,
    can_delete=False
)

MonthlyPriceFormSetEdit = inlineformset_factory(
    Listing,
    MonthlyPrice,
    form=MonthlyPriceForm,
    fields=['month', 'price'],
    extra=0,
    can_delete=False,
)


class EditListingForm(AddListingForm):
    ...


class ListingFilterForm(forms.Form):
    name = forms.CharField(
        required=False, label='Име',
        widget=forms.TextInput(attrs={'placeholder': 'Търси по име'})
    )
    max_people = forms.IntegerField(
        required=False, min_value=1, label='Макс. брой хора',
        widget=forms.NumberInput(attrs={'placeholder': 'Максимален брой хора'})
    )
    city = forms.CharField(
        required=False, label='Град',
        widget=forms.TextInput(attrs={'placeholder': 'Град'})
    )
    amenities = forms.ModelMultipleChoiceField(
        queryset=Amenity.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Удобства'
    )
    price_max = forms.IntegerField(
        required=False, min_value=10, max_value=1000, label='Максимална цена',
        widget=forms.NumberInput()
    )
    check_in = forms.DateField(required=False, widget=forms.HiddenInput())
    check_out = forms.DateField(required=False, widget=forms.HiddenInput())


class CommentForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=[(i, f'{i} Stars') for i in range(1, 6)],
        widget=forms.RadioSelect,
        label="Рейтинг"
    )

    class Meta:
        model = Comment
        fields = ['comment_text', 'rating']
        widgets = {
            'comment_text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Напишете вашия коментар...'}),
        }
        labels = {
            'comment_text': 'Коментар',
        }