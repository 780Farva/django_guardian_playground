from django.contrib.auth import get_user_model
from rest_framework import serializers


class CustomUserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user

    class Meta:
        model = get_user_model()
        fields = ("uuid", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}
