from __future__ import unicode_literals

import logging
import uuid

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from guardian.mixins import GuardianUserMixin
from guardian.models import UserObjectPermission, GroupObjectPermission
from guardian.shortcuts import assign_perm, get_perms
from django.contrib.auth.models import Group

from .managers import UserManager

logger = logging.getLogger("django")


def get_anonymous_user_instance(User):
    return User(email=settings.ANONYMOUS_USER_NAME)


class CustomUser(AbstractBaseUser, PermissionsMixin, GuardianUserMixin):
    """
    A user class implementing a fully featured User model with
    admin-compliant permissions.
    Email and password are required. Other fields are optional.
    A UUID is generated as a secondary key, meant to be used externally.
    """

    uuid = models.UUIDField(
        _("indentifier"), unique=True, blank=False, default=uuid.uuid4
    )
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(_("first name"), max_length=30, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


# when a CustomUser is deleted, remove the object permissions for that user object.
@receiver(pre_delete, sender=CustomUser)
def remove_obj_perms_connected_with_user(sender, instance, **kwargs):
    filters = Q(
        content_type=ContentType.objects.get_for_model(instance), object_pk=instance.pk
    )
    UserObjectPermission.objects.filter(filters).delete()
    GroupObjectPermission.objects.filter(filters).delete()


@receiver(post_save, sender=CustomUser)
def user_post_save(sender, **kwargs):
    """
    Make sure users have the permission to add, change, and delete themselves.
    """
    user, created = kwargs["instance"], kwargs["created"]
    if created and user.email != settings.ANONYMOUS_USER_NAME:
        logger.debug(
            f"Giving {created} change, delete, and view permissions for {user}."
        )
        # Assign model permissions
        assign_perm("users.change_customuser", user)
        assign_perm("users.delete_customuser", user)
        assign_perm("users.view_customuser", user)

        # Assign object permissions on self
        assign_perm("users.change_customuser", user, user)
        assign_perm("users.delete_customuser", user, user)
        assign_perm("users.view_customuser", user, user)

        # Assign object permissions to admins
        admins_group = Group.objects.get(name="admins")
        if not "users.add_customuser" in get_perms(admins_group, user):
            assign_perm("users.add_customuser", admins_group, user)
            assign_perm("users.change_customuser", admins_group, user)
            assign_perm("users.delete_customuser", admins_group, user)
            assign_perm("users.view_customuser", admins_group, user)
            # assign model permissions to admins, just in case
            assign_perm("users.add_customuser", admins_group)
            assign_perm("users.change_customuser", admins_group)
            assign_perm("users.delete_customuser", admins_group)
            assign_perm("users.view_customuser", admins_group)

        if user.is_staff:
            admins_group.user_set.add(user)
