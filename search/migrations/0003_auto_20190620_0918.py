# Generated by Django 2.2.1 on 2019-06-20 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0002_auto_20190620_0917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tvseriesdb',
            name='backdrop_path',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='tvseriesdb',
            name='poster_path',
            field=models.CharField(default='', max_length=255),
        ),
    ]
