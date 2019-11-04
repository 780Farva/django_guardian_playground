from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text="Email is required.")

    class Meta:
        model = get_user_model()
        fields = ("email", "password1", "password2")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = "__all__"
