# Generated by Django 2.2.1 on 2019-07-14 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moviedb', '0020_auto_20190712_1938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='original_title',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='movie',
            name='title',
            field=models.CharField(default='', max_length=255),
        ),
    ]
