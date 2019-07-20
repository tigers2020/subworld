from django.contrib import admin

from subtitle import models


# Register your models here.

class MovieSubtitleAdmin(admin.ModelAdmin):
    list_display = (
        "title", "movie", "language", "rate_good", "rate_bad", "upload_date", "downloaded",
        "comment")
    raw_id_fields = ("movie",)


class TvSubtitleAdmin(admin.ModelAdmin):
    list_display = (
        "title", "tv_series", "tv_season", "tv_episode", "language", "rate_good", "rate_bad", "upload_date", "downloaded",
        "comment")
    raw_id_fields = ("tv_series", 'tv_season', 'tv_episode')


admin.site.register(models.MovieSubtitleInfo, MovieSubtitleAdmin)
admin.site.register(models.TvSubtitleInfo, TvSubtitleAdmin)
