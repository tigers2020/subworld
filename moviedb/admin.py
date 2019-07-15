from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from moviedb import models


# Register your models here.

@admin.register(models.Genre)
class GenreAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name')
    ordering = ('name',)


@admin.register(models.Country)
class CountryAdmin(ImportExportModelAdmin):
    list_display = ("english_name", "iso_3166_1")
    ordering = ('iso_3166_1',)


@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'headquarters', 'homepage', 'logo', 'description',)
    ordering = ('name',)


@admin.register(models.Language)
class LanguageAdmin(ImportExportModelAdmin):
    list_display = ('english_name', 'name', 'iso_639_1')
    ordering = ('english_name',)


@admin.register(models.Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'original_title', 'poster', 'popularity', 'runtime', 'status', 'vote_average')
    readonly_fields = ('poster',)
    ordering = ('-popularity',)
    search_fields = ('title', 'original_title')


@admin.register(models.AlsoKnownAs)
class AlsoKnownAsAdmin(admin.ModelAdmin):
    model = models.AlsoKnownAs
    ordering = ('name',)


@admin.register(models.Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'profile', 'imdb_id', 'known_for_department', 'popularity', 'birthday', 'deathday', 'get_gender',
        'short_biography',
        'homepage')


@admin.register(models.Keyword)
class KeywordAdmin(admin.ModelAdmin):
    model = models.Keyword


@admin.register(models.Videos)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('name', 'site', 'type')


@admin.register(models.Network)
class NetworkAdmin(admin.ModelAdmin):
    list_display = ('name', 'headquarters', 'origin_country')


@admin.register(models.TvEpisode)
class TvEpisodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'air_date',)


@admin.register(models.TvSeason)
class TvSeasonAdmin(admin.ModelAdmin):
    list_display = ('name', 'air_date',)


@admin.register(models.Tv)
class TvAdmin(admin.ModelAdmin):
    list_display = (
        'original_name', 'status', 'in_production', 'last_air_date', 'number_of_episodes', 'number_of_seasons')


@admin.register(models.ExternalID)
class ExternalIDAdmin(admin.ModelAdmin):
    list_display = ('movie_id', 'imdb_id', 'facebook_id', 'instagram_id', 'twitter_id')
    raw_id_fields = ('movie_id',)


@admin.register(models.Credit)
class CreditAdmin(admin.ModelAdmin):
    list_display = ('movie_id', 'tv_id',)
    raw_id_fields = ('movie_id', 'tv_id')


@admin.register(models.Job)
class JobAdmin(ImportExportModelAdmin):
    list_display = ('name',)


@admin.register(models.Jobs)
class JobsAdmin(ImportExportModelAdmin):
    list_display = ('department',)


@admin.register(models.PrimaryTranslations)
class PrimaryTranslationAdmin(ImportExportModelAdmin):
    model = models.PrimaryTranslations


@admin.register(models.Region)
class RegionAdmin(ImportExportModelAdmin):
    model = models.Region


@admin.register(models.Zone)
class ZoneAdmin(ImportExportModelAdmin):
    model = models.Zone


@admin.register(models.TimeZone)
class TimeZoneAdmin(ImportExportModelAdmin):
    model = models.TimeZone


@admin.register(models.Certifications)
class CertificationAdmin(ImportExportModelAdmin):
    model = models.Certifications


@admin.register(models.MovieCertifications)
class MovieCertificationAdmin(ImportExportModelAdmin):
    model = models.MovieCertifications


@admin.register(models.TVCertifications)
class TvCertificationAdmin(ImportExportModelAdmin):
    model = models.TVCertifications


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name',)
