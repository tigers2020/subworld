from ckeditor.fields import RichTextField
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from moviedb.models import Movie, TvSeries, TvSeason, TvEpisode, Language


# Create your models here.

class MovieSubtitleInfo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    title = models.CharField(max_length=1024)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    rate_good = models.IntegerField(default=0)
    rate_bad = models.IntegerField(default=0)
    upload_date = models.DateTimeField(auto_now_add=True)
    downloaded = models.IntegerField(default=0)
    comment = RichTextField(blank=True, null=True)


class TvSubtitleInfo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tv_series = models.ForeignKey(TvSeries, on_delete=models.CASCADE)
    tv_season = models.ForeignKey(TvSeason, on_delete=models.CASCADE)
    tv_episode = models.ForeignKey(TvEpisode, on_delete=models.CASCADE)
    title = models.CharField(max_length=1024)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    rate_good = models.IntegerField(default=0)
    rate_bad = models.IntegerField(default=0)
    upload_date = models.DateTimeField(auto_now_add=True)
    downloaded = models.IntegerField(default=0)
    comment = RichTextField(blank=True, null=True)


class MovieSubtitles(models.Model):
    file = models.FileField()
    info = models.ForeignKey(MovieSubtitleInfo, on_delete=models.CASCADE)


class TvSubtitles(models.Model):
    file = models.FileField()
    info = models.ForeignKey(TvSubtitleInfo, on_delete=models.CASCADE)
