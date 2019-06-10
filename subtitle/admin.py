from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from subtitle import models


# Register your models here.


class LanguageAdmin(ImportExportModelAdmin):
    list_display = ("iso_language_name", "language_family", "native_name", "iso_639_1", "notes")
    ordering = ("iso_language_name",)


class SubtitleAdmin(admin.ModelAdmin):
    list_display = ("title", "db_id", "type",  "language", "rate_star", "rate_good", "rate_bad", "upload_date", "downloaded", "sub_file","comment")


admin.site.register(models.Language, LanguageAdmin)
admin.site.register(models.Subtitle, SubtitleAdmin)
