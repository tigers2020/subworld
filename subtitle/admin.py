from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from subtitle import models


# Register your models here.


class LanguageAdmin(ImportExportModelAdmin):
    list_display = ("language_family", "iso_language_name", "native_name", "iso_639_1", "notes")


class RipAdmin(admin.ModelAdmin):
    list_display = ("name",)


class SubtitleAdmin(admin.ModelAdmin):
    list_display = ("db_id", "title", "sub_file", "language", "resolution", "rip", "author", "comment")


admin.site.register(models.Language, LanguageAdmin)
admin.site.register(models.Rip, RipAdmin)
admin.site.register(models.Subtitle, SubtitleAdmin)
