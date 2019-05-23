from django.db import models

# Create your models here.

class language(models.Model):
    name = models.CharField(max_length=255)
    ori_name = models.CharField(max_length=255)
    iso = models.CharField(max_length=255)
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

class Subtitle(models.Model):
    db_id = models.IntegerField()
    title = models.CharField(max_length=255)
    sub_file = models.FileField()
    language = models.ForeignKey(language, on_delete=models.CASCADE)
    resolution = models.CharField( max_length=255)
    rip = models.CharField(default='', max_length=255)
    release = models.CharField( max_length=255)
    author = models.CharField(max_length=255)
    comment = models.TextField(max_length=255)

