# Generated by Django 2.2.1 on 2019-07-20 00:39

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('moviedb', '0004_auto_20190719_2013'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='video',
            managers=[
            ],
        ),
        migrations.CreateModel(
            name='Videos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField(blank=True, null=True)),
                ('movie', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='movie+', to='moviedb.Movie')),
                ('tv_series', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tv_series+', to='moviedb.TvSeries')),
                ('videos', models.ManyToManyField(related_name='_videos_videos_+', to='moviedb.Video')),
            ],
            managers=[
                ('movie_initialize', django.db.models.manager.Manager()),
            ],
        ),
    ]
