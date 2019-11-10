import logging

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

logger = logging.getLogger(__name__)
logging.disable(logging.NOTSET)
logger.setLevel(logging.DEBUG)


class UsersTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin_password = "askdfhaskf"
        cls.admin_user = get_user_model().objects.create_user(
            email="admin@ljkahsdbmfnas.com", password=cls.admin_password, is_staff=True
        )
        cls.user_password = "9823475tyuegrfhjdksis"
        cls.user = get_user_model().objects.create_user(
            email="36@09834.com", password=cls.user_password, is_staff=False
        )
        cls.anonymous = get_user_model().objects.get(email="Anonymous@anonymous.com")

    def setUp(self):
        self.client = APIClient()

    def tearDown(self):
        self.client.logout()

    def login_as_admin(self):
        self.client.login(username=self.admin_user.email, password=self.admin_password)

    def login_as_user(self):
        self.client.login(username=self.user.email, password=self.user_password)

    def login_as_anonymous(self):
        self.client.login(username=self.anonymous.email, password="")


class ListUsersTest(UsersTest):
    def test_guardian_anon_user_cant_list_all(self):
        self.login_as_anonymous()
        result = self.client.get("/users/", format="json")
        self.assertEqual(result.status_code, status.HTTP_403_FORBIDDEN)

    def test_anon_user_cant_list_all(self):
        result = self.client.get("/users/", format="json")
        self.assertEqual(result.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_user_can_list_all(self):
        self.login_as_admin()
        result = self.client.get("/users/", format="json")
        self.assertEqual(result.status_code, status.HTTP_200_OK)

    def test_non_admin_just_gets_self(self):
        self.login_as_user()
        result = self.client.get("/users/", format="json")
        self.assertEqual(1, len(result.data))
        self.assertContains(result, self.user.uuid)
        self.assertEqual(result.status_code, status.HTTP_200_OK)

    def test_admin_user_can_list_specific(self):
        self.login_as_admin()
        result = self.client.get(f"/users/{self.user.uuid}/", format="json")
        self.assertEqual(result.status_code, status.HTTP_200_OK)

    def test_anon_user_cant_list_specific(self):
        result = self.client.get(f"/users/{self.user.uuid}/", format="json")
        self.assertEqual(result.status_code, status.HTTP_403_FORBIDDEN)

    def test_guardian_anon_user_cant_list_specific(self):
        self.login_as_anonymous()
        result = self.client.get(f"/users/{self.user.uuid}/", format="json")
        self.assertEqual(result.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_list_self(self):
        self.login_as_user()
        result = self.client.get(f"/users/{self.user.uuid}/", format="json")
        print(f"result: {result.data}")
        self.assertEqual(result.status_code, status.HTTP_200_OK)

    def test_user_cant_list_other_user(self):
        self.login_as_user()
        result = self.client.get(f"/users/{self.admin_user.uuid}/", format="json")
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)


class CreateUserTest(UsersTest):
    def test_anon_user_can_create(self):
        self.assertEqual(
            get_user_model().objects.filter(email="237485jhdf@snmgflk.com").count(), 0
        )
        result = self.client.post(
            f"/users/",
            {"email": "237485jhdf@snmgflk.com", "password": "30945akhjudf"},
            format="json",
        )
        logger.debug(result.data)
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(
            get_user_model().objects.filter(email="237485jhdf@snmgflk.com").count(), 1
        )
