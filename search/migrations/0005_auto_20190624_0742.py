# Generated by Django 2.2.1 on 2019-06-24 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0004_auto_20190623_2059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persondb',
            name='backdrop_path',
            field=models.CharField(default='', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='persondb',
            name='poster_path',
            field=models.CharField(default='', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='tvseriesdb',
            name='backdrop_path',
            field=models.CharField(default='', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='tvseriesdb',
            name='poster_path',
            field=models.CharField(default='', max_length=255, null=True),
        ),
    ]
