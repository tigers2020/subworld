from django.db import models

# Create your models here.

class language(models.Model):
    name = models.CharField()
    ori_name = models.CharField()
    iso = models.CharField()
Rip = {
    "TS",
    "DVDScr",
    "DVDRip",
    "Bluray",
    "BrRip",
    "BDRip",
    "HDRip",
    "720p.BlueRay",
    "1080p.BlueRay",
    "WEB",
    "WEBRip",
    "WEB-DL",
    "HDCAM",
    "HDVDRip",
    "WEB-HD",
    "m-HD",
    "R5",
    "TC",
    "HQCAM",
    "HD-TS"

}
RESOLUTION = (
    (1, "320p"),
    (2, "480p"),
    (3, "720p"),
    (4, "1080i"),
    (5, "1080p"),
    (6, "2k"),
    (7, "4k")

)
class Subtitle(models.Model):
    db_id = models.IntegerField()
    title = models.CharField(max_length=255)
    sub_file = models.FileField()
    language = models.ForeignKey(language, on_delete=models.CASCADE)
    resolution = models.CharField(choices=RESOLUTION)
    rip = models.CharField(choices=Rip, default='')
    release = models.CharField()
    author = models.CharField()
    comment = models.TextField()

