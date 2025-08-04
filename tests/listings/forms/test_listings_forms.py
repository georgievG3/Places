from datetime import date

from django.test import TestCase
from accounts.models import AppUser
from listings.forms import AddListingForm, AddListingLocationForm, AddListingAmenityForm, MonthlyPriceForm, \
    ListingFilterForm
from listings.models import Location, Amenity, Camping


class TestListingForms(TestCase):

    def setUp(self):
        self.user = AppUser.objects.create_user(
            email='testuser@example.com',
            password='password123',
            first_name='Test',
            last_name='User',
        )

        self.location = Location.objects.create(
            region='Югозападен',
            address='ул. Морска 1',
            city='Созопол',
            latitude=42.419,
            longitude=27.695,
            terrain_type='sea'
        )

        self.amenity = Amenity.objects.create(name='Wi-Fi')

        self.camping = Camping.objects.create(
            name='Къмпинг Златна Рибка',
            description='Това е дълго описание на къмпинга, което съдържа поне 50 символа.',
            location=self.location
        )

    def test__add__listings__form__is_valid__success(self):
        form = AddListingForm(data={
            'title': 'Каравана до морето',
            'mini_description': 'Гледка към морето',
            'type': 'camper',
            'location': self.location.id,
            'camping': self.camping.id,
            'rooms': 2,
            'pets_allowed': True,
            'min_nights': 2,
            'max_people': 4,
            'square_meters': 20,
            'description': 'Уникална каравана с всички удобства, подходяща за семейства.',
            'regular_price': 120.00,
            'owner': self.user.id,
        })
        self.assertTrue(form.is_valid(), form.errors)

    def test__location__form__is_valid_success(self):
        form = AddListingLocationForm(data={
            'region': 'Югозападен',
            'address': 'ул. Морска 1',
            'city': 'Созопол',
            'latitude': 42.419,
            'longitude': 27.695,
            'terrain_type': 'sea'
        })
        self.assertTrue(form.is_valid(), form.errors)

    def test__amenity__form__is_valid_success(self):
        form = AddListingAmenityForm(data={'name': 'Барбекю'})
        self.assertTrue(form.is_valid(), form.errors)

    def test__monthly_price_form__is_valid_success(self):
        form = MonthlyPriceForm(data={
            'month': 5,
            'price': 150.00
        })
        self.assertTrue(form.is_valid(), form.errors)

    def test__listing_filter_form__is_valid_success(self):
        form = ListingFilterForm(data={
            'name': 'Каравана',
            'max_people': 4,
            'city': 'Созопол',
            'amenities': [self.amenity.id],
            'price_max': 200,
            'check_in': date.today(),
            'check_out': date.today()
        })
        self.assertTrue(form.is_valid(), form.errors)
