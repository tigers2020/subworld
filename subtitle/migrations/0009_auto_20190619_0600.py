# Generated by Django 2.2.1 on 2019-06-19 10:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('subtitle', '0008_auto_20190618_1913'),
    ]

    operations = [
        migrations.AddField(
            model_name='tvsubtitle',
            name='episode_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tvsubtitle',
            name='season_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='moviesubtitle',
            name='db_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search.MovieDB'),
        ),
        migrations.AlterField(
            model_name='tvsubtitle',
            name='db_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search.TvSeriesDB'),
        ),
    ]
