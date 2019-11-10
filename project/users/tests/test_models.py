from django.contrib.auth import get_user_model
from django.test import TestCase

from users.models import CustomUser
from users.models import get_anonymous_user_instance


class AnonymousUserPermissionsTest(TestCase):
    def setUp(self):
        self.other_user = CustomUser.objects.create_user(
            email="other@duper.com", password="98743uhgjdf"
        )
        self.anonymous = get_user_model().objects.get(email="Anonymous@anonymous.com")

    def test_anonymous_permissions(self):
        # anonymous users can sign up new users
        # handled by modelbackend, not guardian
        # self.assertTrue(self.anonymous.has_perm("add_customuser"))

        # anonymous users can't do anything else to users, really.
        self.assertFalse(self.anonymous.has_perm("add_permission"))
        self.assertFalse(self.anonymous.has_perm("change_permission"))
        self.assertFalse(self.anonymous.has_perm("delete_permission"))
        self.assertFalse(self.anonymous.has_perm("view_permission"))

        self.assertFalse(self.anonymous.has_perm("change_customuser", self.other_user))
        self.assertFalse(self.anonymous.has_perm("delete_customuser", self.other_user))
        self.assertFalse(self.anonymous.has_perm("view_customuser", self.other_user))


class CustomUserPermissionsTest(TestCase):
    def setUp(self):
        admin = CustomUser.objects.create_superuser(
            email="super@duper.com", password="asdlfjaslughf"
        )

        user = CustomUser.objects.create_user(
            email="user@duper.com", password="asdfasfgsdfgdfgg"
        )

        other_user = CustomUser.objects.create_user(
            email="other@duper.com", password="98743uhgjdf"
        )

        # Request the users again to ensure the cached permissions on them get busted
        self.admin = CustomUser.objects.get(email=admin.email)
        self.user = CustomUser.objects.get(email=user.email)
        self.other_user = CustomUser.objects.get(email=other_user.email)

    def test_admin_permissions(self):
        self.assertTrue(self.admin.has_perm("add_user"))
        self.assertTrue(self.admin.has_perm("add_customuser"))

        self.assertTrue(self.admin.has_perm("add_permission"))
        self.assertTrue(self.admin.has_perm("change_permission"))
        self.assertTrue(self.admin.has_perm("delete_permission"))
        self.assertTrue(self.admin.has_perm("view_permission"))

        self.assertTrue(self.admin.has_perm("change_customuser", self.user))
        self.assertTrue(self.admin.has_perm("delete_customuser", self.user))
        self.assertTrue(self.admin.has_perm("view_customuser", self.user))

        self.assertTrue(self.admin.has_perm("change_customuser", self.other_user))
        self.assertTrue(self.admin.has_perm("delete_customuser", self.other_user))
        self.assertTrue(self.admin.has_perm("view_customuser", self.other_user))

    def test_user_permissions(self):
        # normal users can't add users
        self.assertFalse(self.user.has_perm("add_user"))
        self.assertFalse(self.user.has_perm("add_customuser"))

        # normal users can't add users mess with permissions
        self.assertFalse(self.user.has_perm("add_permission"))
        self.assertFalse(self.user.has_perm("change_permission"))
        self.assertFalse(self.user.has_perm("delete_permission"))
        self.assertFalse(self.user.has_perm("view_permission"))
        self.assertFalse(self.user.has_perm("add_permission", self.user))
        self.assertFalse(self.user.has_perm("change_permission", self.user))
        self.assertFalse(self.user.has_perm("delete_permission", self.user))
        self.assertFalse(self.user.has_perm("view_permission", self.user))

        # check that normal users have model permissions
        self.assertTrue(self.user.has_perm("users.change_customuser"))
        self.assertTrue(self.user.has_perm("users.delete_customuser"))
        self.assertTrue(self.user.has_perm("users.view_customuser"))

        # normal users can change and delete themselves, once guardian has given them permission
        self.assertTrue(self.user.has_perm("change_customuser", self.user))
        self.assertTrue(self.user.has_perm("delete_customuser", self.user))
        self.assertTrue(self.user.has_perm("view_customuser", self.user))
        self.assertTrue(self.user.has_perm("users.change_customuser", self.user))
        self.assertTrue(self.user.has_perm("users.delete_customuser", self.user))
        self.assertTrue(self.user.has_perm("users.view_customuser", self.user))

        # normal users can't change other users or their permissions
        self.assertFalse(self.user.has_perm("change_customuser", self.other_user))
        self.assertFalse(self.user.has_perm("delete_customuser", self.other_user))
        self.assertFalse(self.user.has_perm("view_customuser", self.other_user))
        self.assertFalse(self.user.has_perm("add_permission", self.other_user))
        self.assertFalse(self.user.has_perm("change_permission", self.other_user))
        self.assertFalse(self.user.has_perm("delete_permission", self.other_user))
        self.assertFalse(self.user.has_perm("view_permission", self.other_user))


class CustomUserUuidTest(TestCase):
    def test_username_is_email(self):
        user = CustomUser.objects.create_user(
            email="2387594@ljkh.com", password="lsdjfoiuwe"
        )
        self.assertEqual(user.USERNAME_FIELD, "email")

    def test_user_gets_uuid(self):
        user = CustomUser.objects.create_user(
            email="alskdf@lkjasd.com", password="lsdjfoiuwe"
        )
        self.assertIsNotNone(user.uuid)


class AnonyousUserTest(TestCase):
    def test_returns_anonymous_user(self):
        user = get_anonymous_user_instance(CustomUser)
        self.assertEqual(user.email, "Anonymous@anonymous.com")
        self.assertFalse(user.is_staff)
