# Generated by Django 2.2.1 on 2019-07-12 02:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moviedb', '0008_auto_20190711_0611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='backdrop_path',
            field=models.CharField(default='', max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='budget',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='movie',
            name='original_language',
            field=models.CharField(default='', max_length=4),
        ),
        migrations.AlterField(
            model_name='movie',
            name='original_title',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AlterField(
            model_name='movie',
            name='popularity',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='movie',
            name='release_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='revenue',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='movie',
            name='status',
            field=models.CharField(choices=[('Rumored', 'Rumored'), ('Planned', 'Planned'), ('InProduction', 'In Production'), ('PostProduction', 'Post Production'), ('Released', 'Released'), ('Canceled', 'Canceled')], default='', max_length=32),
        ),
        migrations.AlterField(
            model_name='movie',
            name='title',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AlterField(
            model_name='movie',
            name='vote_average',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='movie',
            name='vote_count',
            field=models.IntegerField(default=0),
        ),
    ]