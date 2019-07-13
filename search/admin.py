from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from search import models


# Register your models here.


class MovieDBAdmin(admin.ModelAdmin):
    list_display = ('title', "original_title", "id", "poster_path", "backdrop_path", "adult", "popularity", "video")
    search_fields = ("original_title", 'title')
    ordering = ('-popularity',)


class GenreDBAdmin(admin.ModelAdmin):
    list_display = ("name",)


class CollectionDBAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


class KeywordDBAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


class PersonDBAdmin(admin.ModelAdmin):
    list_display = ("name", "adult", "popularity")
    search_fields = ("name",)
    ordering = ('-popularity',)


class ProductionCompanyDBAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


class TvSeriesDBAdmin(admin.ModelAdmin):
    list_display = ('name', "original_name", "poster_path", "backdrop_path", "popularity")
    search_fields = ("original_name", 'name',)
    ordering = ('-popularity',)


admin.site.register(models.MovieDB, MovieDBAdmin)
admin.site.register(models.CollectionDB, CollectionDBAdmin)
admin.site.register(models.KeywordDB, KeywordDBAdmin)
admin.site.register(models.PersonDB, PersonDBAdmin)
admin.site.register(models.ProductionCompanyDB, ProductionCompanyDBAdmin)
admin.site.register(models.TvSeriesDB, TvSeriesDBAdmin)
admin.site.register(models.GenreDB, GenreDBAdmin)
