# Generated by Django 2.2.1 on 2019-06-20 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subtitle', '0011_auto_20190620_1949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tvsubtitle',
            name='upload_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
