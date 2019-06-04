from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Language(models.Model):
    language_family = models.CharField(max_length=126)
    iso_language_name = models.CharField(max_length=255)
    native_name = models.CharField(max_length=255)
    iso_639_1 = models.CharField(max_length=8)
    iso_639_2_t = models.CharField(max_length=8)
    iso_639_2_b = models.CharField(max_length=8)
    iso_639_3 = models.CharField(max_length=8, null=True)
    notes = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.iso_language_name + '[' + self.native_name + ']'


class Rip(models.Model):
    name = models.CharField(max_length=16)

    def __str__(self):
        return self.name


class Resolution(models.Model):
    name = models.CharField(max_length=80)
    screen_w = models.IntegerField()
    screen_h = models.IntegerField()
    aspect_ratio = models.CharField(max_length=16)
    total_pixel_count = models.IntegerField()

    def __str__(self):
        name = "{0} ({1} x {2})".format(self.name, self.screen_w, self.screen_h)
        return name


class Subtitle(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    type = models.IntegerField()
    db_id = models.IntegerField()
    title = models.CharField(max_length=255)
    sub_file = models.FileField()
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    resolution = models.ForeignKey(Resolution, on_delete=models.CASCADE)
    rip = models.ForeignKey(Rip, on_delete=models.CASCADE)
    rate_good = models.IntegerField(default=0)
    rate_bad = models.IntegerField(default=0)
    release = models.DateField(null=True )
    author = models.CharField(max_length=255)
    downloaded = models.IntegerField(default=0)
    comment = models.TextField(max_length=255, null=True)

    def __str__(self):
        return self.title
