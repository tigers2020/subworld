# Generated by Django 2.2.1 on 2019-06-20 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='moviedb',
            name='backdrop_path',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='moviedb',
            name='poster_path',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='persondb',
            name='backdrop_path',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='persondb',
            name='poster_path',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='tvseriesdb',
            name='backdrop_path',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tvseriesdb',
            name='poster_path',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
