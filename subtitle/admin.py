from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from subtitle import models


# Register your models here.


class LanguageAdmin(ImportExportModelAdmin):
    list_display = ("iso_language_name", "language_family", "native_name", "iso_639_1", "notes")
    ordering = ("iso_language_name",)


class ResolutionAdmin(ImportExportModelAdmin):
    list_display = ("name", "screen_w", "screen_h", "aspect_ratio", "total_pixel_count")


class RipAdmin(ImportExportModelAdmin):
    list_display = ("name",)


class SubtitleAdmin(admin.ModelAdmin):
    list_display = ("db_id", "title", "sub_file", "language", "resolution", "rip", "author", "comment")


admin.site.register(models.Language, LanguageAdmin)
admin.site.register(models.Rip, RipAdmin)
admin.site.register(models.Subtitle, SubtitleAdmin)
admin.site.register(models.Resolution, ResolutionAdmin)
