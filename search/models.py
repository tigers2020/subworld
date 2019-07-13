from django.db import models


# Create your models here.

class MovieDB(models.Model):
    adult = models.BooleanField(default=False)
    title = models.CharField(max_length=255, null=True)
    original_title = models.CharField(max_length=255)
    poster_path = models.CharField(max_length=255, default="", null=True)
    backdrop_path = models.CharField(max_length=255, default="", null=True)
    popularity = models.FloatField()
    video = models.BooleanField(default=False)

    def __str__(self):
        return self.original_title


class GenreDB(models.Model):
    name = models.CharField(max_length=126)

    def __str__(self):
        return self.name


class CollectionDB(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class KeywordDB(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class PersonDB(models.Model):
    adult = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    poster_path = models.CharField(max_length=255, default="", null=True)
    backdrop_path = models.CharField(max_length=255, default="", null=True)
    popularity = models.FloatField()

    def __str__(self):
        return self.name


class ProductionCompanyDB(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class TvNetworkDB(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class TvSeriesDB(models.Model):
    original_name = models.CharField(max_length=255)
    name = models.CharField(max_length=255, null=True)
    poster_path = models.CharField(max_length=255, default="", null=True)
    backdrop_path = models.CharField(max_length=255, default="", null=True)
    popularity = models.FloatField()

    def __str__(self):
        return self.original_name
