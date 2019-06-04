from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import SubUser

class SubUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = SubUser
        fields = ("username", "email")

class SubUserChangeForm(UserChangeForm):

    class Meta:
        model = SubUser
        fields = UserChangeForm.Meta.fields