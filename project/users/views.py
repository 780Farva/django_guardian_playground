from rest_framework.permissions import DjangoObjectPermissions
from rest_framework.viewsets import ModelViewSet

from users.models import CustomUser
from users.serializers import CustomUserSerializer


class CustomObjectPermissions(DjangoObjectPermissions):
    """
    Similar to `DjangoObjectPermissions`, but adding 'view' permissions.
    """

    perms_map = {
        "GET": ["%(app_label)s.view_%(model_name)s"],
        "OPTIONS": ["%(app_label)s.view_%(model_name)s"],
        "HEAD": ["%(app_label)s.view_%(model_name)s"],
        "POST": ["%(app_label)s.add_%(model_name)s"],
        "PUT": ["%(app_label)s.change_%(model_name)s"],
        "PATCH": ["%(app_label)s.change_%(model_name)s"],
        "DELETE": ["%(app_label)s.delete_%(model_name)s"],
    }


class CustomUserViewSet(ModelViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """

    lookup_field = "uuid"
    # must match exactly this regex pattern, including hyphens in their particular places
    lookup_value_regex = "[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
    serializer_class = CustomUserSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return CustomUser.objects.all()
        return CustomUser.objects.filter(email=user.email)

    permission_classes = [CustomObjectPermissions]
