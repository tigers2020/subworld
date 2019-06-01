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


class Subtitle(models.Model):
    type = models.IntegerField()
    db_id = models.IntegerField()
    title = models.CharField(max_length=255)
    sub_file = models.FileField()
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    resolution = models.CharField(max_length=255)
    rip = models.ForeignKey(Rip, on_delete=models.CASCADE)
    release = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    comment = models.TextField(max_length=255)

    def __str__(self):
        return self.title
