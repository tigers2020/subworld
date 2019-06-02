from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from search import models


# Register your models here.


class MovieDBAdmin(ImportExportModelAdmin):
    list_display = ("original_title", "id", "adult", "popularity", "video")


class GenreDBAdmin(ImportExportModelAdmin):
    list_display = ("name",)


class CollectionDBAdmin(ImportExportModelAdmin):
    list_display = ("name",)


class KeywordDBAdmin(ImportExportModelAdmin):
    list_display = ("name",)


class PersonDBAdmin(ImportExportModelAdmin):
    list_display = ("name", "adult", "popularity")


class ProductionCompanyDBAdmin(ImportExportModelAdmin):
    list_display = ("name",)


class TvSeriesDBAdmin(ImportExportModelAdmin):
    list_display = ("original_name", "popularity")


admin.site.register(models.MovieDB, MovieDBAdmin)
admin.site.register(models.CollectionDB, CollectionDBAdmin)
admin.site.register(models.KeywordDB, KeywordDBAdmin)
admin.site.register(models.PersonDB, PersonDBAdmin)
admin.site.register(models.ProductionCompanyDB, ProductionCompanyDBAdmin)
admin.site.register(models.TvSeriesDB, TvSeriesDBAdmin)
admin.site.register(models.GenreDB, GenreDBAdmin)
