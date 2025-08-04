from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

UserModel = get_user_model()

class TestUserProfile(TestCase):
    def setUp(self):
        self.email = 'test@test.com'
        self.password = 'test123'

        self.user = UserModel.objects.create_user(
            email=self.email,
            password=self.password,
            first_name='test',
            last_name='test',
        )

        self.profile = self.user.profile
        self.profile.phone_number = '0896758491'
        self.profile.date_of_birth = date(1990, 12, 31)
        self.profile.save()

    def test__profile__creation(self):
        self.assertEqual(self.profile.user.email, 'test@test.com')
        self.assertEqual(self.profile.phone_number, '0896758491')
        self.assertEqual(self.profile.date_of_birth.strftime('%Y-%m-%d'), '1990-12-31')

    def test__profile__is_complete__true(self):
        self.assertTrue(self.profile.is_complete())

    def test__profile__is_complete__false__missing__phone(self):
        self.profile.phone_number = ''
        self.profile.save()
        self.assertFalse(self.profile.is_complete())

    def test__profile_is_complete__false_missing__birth_date(self):
        self.profile.date_of_birth = None
        self.profile.save()
        self.assertFalse(self.profile.is_complete())

    def test__date_of_birth__validator__invalid_age(self):
        too_young_date = date.today() - timedelta(days=365 * 10)
        self.profile.date_of_birth = too_young_date
        with self.assertRaises(ValidationError):
            self.profile.full_clean()

    def test__phone_number__min_length__validation(self):
        self.profile.phone_number = '123'
        with self.assertRaises(ValidationError):
            self.profile.full_clean()
