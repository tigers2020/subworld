# Generated by Django 2.2.1 on 2019-07-12 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moviedb', '0014_auto_20190712_1654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='homepage',
            field=models.URLField(null=True),
        ),
    ]