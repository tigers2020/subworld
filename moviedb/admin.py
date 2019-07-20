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
    search_fields = ('name',)
    autocomplete_fields = ('parent_company',)


#
# @admin.register(models.Language)
# class LanguageAdmin(ImportExportModelAdmin):
#     list_display = ('english_name', 'name', 'iso_639_1')
#     ordering = ('english_name',)


@admin.register(models.Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'original_title', 'poster', 'popularity', 'runtime', 'status', 'vote_average')
    readonly_fields = ('poster',)
    ordering = ('-id',)
    search_fields = ('title', 'original_title')
    autocomplete_fields = ('production_companies', 'keyword',)


@admin.register(models.Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'profile', 'imdb_id', 'known_for_department', 'popularity', 'birthday', 'deathday', 'get_gender',
        'short_biography',
        'homepage')
    search_fields = ('name',)


@admin.register(models.Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('english_name', 'name', 'iso_639_1',)


@admin.register(models.Keyword)
class KeywordAdmin(admin.ModelAdmin):
    model = models.Keyword
    search_fields = ('name', )


@admin.register(models.Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('name', 'site', 'type')


@admin.register(models.Network)
class NetworkAdmin(admin.ModelAdmin):
    list_display = ('name', 'headquarters', 'origin_country')
    search_fields = ('name', 'headquarters',)


@admin.register(models.TvEpisode)
class TvEpisodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'air_date',)
    search_fields = ('name',)


@admin.register(models.TvSeason)
class TvSeasonAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'air_date',)
    search_fields = ('name',)


@admin.register(models.TvSeries)
class TvAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'original_name', 'status', 'in_production', 'last_air_date', 'number_of_episodes',
        'number_of_seasons')
    search_fields = ('name', 'original_name',)
    autocomplete_fields = ('created_by', 'networks', 'production_companies', 'seasons',)


@admin.register(models.ExternalID)
class ExternalIDAdmin(admin.ModelAdmin):
    list_display = ('movie_id', 'imdb_id', 'facebook_id', 'instagram_id', 'twitter_id')
    raw_id_fields = ('movie_id',)


@admin.register(models.Credit)
class CreditAdmin(admin.ModelAdmin):
    list_display = ('movie', 'tv_series',)
    raw_id_fields = ('movie', 'tv_series')


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    autocomplete_fields = ('parts',)
    search_fields = ('name',)
