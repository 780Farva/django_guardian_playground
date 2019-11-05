from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from rest_framework.routers import SimpleRouter
from users.views import CustomUserViewSet


router = SimpleRouter()
router.register(r"users", CustomUserViewSet, basename="user")

urlpatterns = [
    url(r"^", include(router.urls)),
    path('admin/', admin.site.urls),
]
