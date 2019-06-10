from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField


# Create your models here.
from django.urls import reverse


class Language(models.Model):
    language_family = models.CharField(max_length=126)
    iso_language_name = models.CharField(max_length=255)
    native_name = models.CharField(max_length=255)
    iso_639_1 = models.CharField(max_length=8)
    iso_639_2_t = models.CharField(max_length=8)
    iso_639_2_b = models.CharField(max_length=8)
    iso_639_3 = models.CharField(max_length=8, null=True)
    notes = RichTextField(null=True)

    def __str__(self):
        return self.iso_language_name + '[' + self.native_name + ']'


class Subtitle(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    type = models.IntegerField()
    db_id = models.IntegerField()
    title = models.CharField(max_length=255)
    sub_file = models.FileField()
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    rate_star = models.IntegerField(default=0)
    rate_good = models.IntegerField(default=0)
    rate_bad = models.IntegerField(default=0)
    upload_date = models.DateTimeField(auto_now_add=True)
    downloaded = models.IntegerField(default=0)
    comment = RichTextField(blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("subtitle:movie_detail", kwargs={"id": self.db_id})


