# Generated by Django 2.2.1 on 2019-07-12 20:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moviedb', '0011_person_popularity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='genre',
            name='media_type',
        ),
    ]
