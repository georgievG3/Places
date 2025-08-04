from django.db import IntegrityError
from django.test import TestCase

from django.contrib.auth import get_user_model

UserModel = get_user_model()

class UserModelTestCase(TestCase):

    def setUp(self):
        self.email = 'test@test.com'
        self.password = 'test123'

        self.user = UserModel.objects.create_user(
            email = self.email,
            password = self.password,
            first_name = 'test',
            last_name = 'test',
        )

    def test__unique_emails__raise_integrityerror(self):

        with self.assertRaises(IntegrityError) as ie:
            user2 = UserModel.objects.create_user(
                email=self.email,
                password=self.password,
                first_name='test2',
                last_name='test2',
            )

        self.assertEqual(str(ie.exception), str(ie.exception))



