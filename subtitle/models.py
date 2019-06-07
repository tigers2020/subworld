from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField


# Create your models here.

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
    user = models.IntegerField()
    type = models.IntegerField()
    db_id = models.IntegerField()
    title = models.CharField(max_length=255)
    sub_file = models.FileField()
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    run_time = models.DurationField(null=True)
    rate_star = models.IntegerField(default=0)
    rate_good = models.IntegerField(default=0)
    rate_bad = models.IntegerField(default=0)
    upload_date = models.DateTimeField(auto_now_add=True)
    downloaded = models.IntegerField(default=0)
    comment = RichTextField()

    def __str__(self):
        return self.title
