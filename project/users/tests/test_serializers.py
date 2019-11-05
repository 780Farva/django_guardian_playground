from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase

from users.serializers import CustomUserSerializer


class CreateUserSerializerTest(TestCase):
    def test_creates_a_user(self):
        data = {"email": "someone@somewhere.ca", "password": "ohdangapassword"}

        user_count = len(get_user_model().objects.exclude(email=settings.ANONYMOUS_USER_NAME))
        self.assertEqual(user_count, 0)

        serializer = CustomUserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save()

        user_count = len(get_user_model().objects.exclude(email=settings.ANONYMOUS_USER_NAME))
        self.assertEqual(user_count, 1)

        user = get_user_model().objects.exclude(email=settings.ANONYMOUS_USER_NAME).first()
        self.assertEqual("someone@somewhere.ca", user.email)
