from django.contrib.auth.models import AbstractUser, UserManager


# Create your models here.


class SubUserManager(UserManager):
    pass


class SubUser(AbstractUser):
    objects = SubUserManager()