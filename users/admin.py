from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import SubUserCreationForm, SubUserChangeForm
from .models import SubUser
# Register your models here.


class SubUserAdmin(UserAdmin):
    model = SubUser
    add_form = SubUserCreationForm
    form = SubUserChangeForm

admin.site.register(SubUser, SubUserAdmin)
