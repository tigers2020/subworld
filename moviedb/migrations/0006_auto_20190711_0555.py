# Generated by Django 2.2.1 on 2019-07-11 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moviedb', '0005_language_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='language',
            name='english_name',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='language',
            name='iso_639_1',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='language',
            name='name',
            field=models.CharField(max_length=64),
        ),
    ]