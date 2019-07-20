# Generated by Django 2.2.1 on 2019-07-19 01:13

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import moviedb.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(default='', null=True)),
                ('headquarters', models.CharField(default='', max_length=255)),
                ('homepage', models.URLField(null=True)),
                ('logo_path', models.CharField(max_length=64, null=True)),
                ('name', models.CharField(default='', max_length=1024)),
            ],
            bases=(models.Model, moviedb.models.TmdbInitMixin),
            managers=[
                ('initialize', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iso_3166_1', models.CharField(max_length=2, unique=True)),
                ('english_name', models.CharField(max_length=16)),
                ('note', models.CharField(blank=True, max_length=1024, null=True)),
            ],
            managers=[
                ('initialize', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
            bases=(models.Model, moviedb.models.TmdbInitMixin),
            managers=[
                ('initialize', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
            managers=[
                ('initialize', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iso_639_1', models.CharField(max_length=64, unique=True)),
                ('english_name', models.CharField(max_length=64)),
                ('name', models.CharField(max_length=64, null=True)),
            ],
            managers=[
                ('initialize', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adult', models.BooleanField(default=False)),
                ('backdrop_path', models.CharField(default='', max_length=128, null=True)),
                ('budget', models.BigIntegerField(default=0)),
                ('homepage', models.URLField(max_length=2048, null=True)),
                ('imdb_id', models.CharField(max_length=16, null=True)),
                ('original_title', models.CharField(default='', max_length=1024)),
                ('overview', models.TextField(null=True)),
                ('popularity', models.FloatField(default=0)),
                ('poster_path', models.CharField(max_length=128, null=True)),
                ('release_date', models.DateField(null=True)),
                ('revenue', models.BigIntegerField(default=0)),
                ('runtime', models.IntegerField(null=True)),
                ('status', models.CharField(choices=[('Rumored', 'Rumored'), ('Planned', 'Planned'), ('InProduction', 'In Production'), ('PostProduction', 'Post Production'), ('Released', 'Released'), ('Canceled', 'Canceled')], default='', max_length=32)),
                ('tagline', models.CharField(max_length=1024, null=True)),
                ('title', models.CharField(default='', max_length=1024)),
                ('video', models.BooleanField(default=False)),
                ('vote_average', models.FloatField(default=0)),
                ('vote_count', models.IntegerField(default=0)),
                ('genres', models.ManyToManyField(related_name='_movie_genres_+', to='moviedb.Genre')),
                ('keyword', models.ManyToManyField(null=True, related_name='_movie_keyword_+', to='moviedb.Keyword')),
                ('original_language', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='moviedb.Language', to_field='iso_639_1')),
                ('production_companies', models.ManyToManyField(related_name='_movie_production_companies_+', to='moviedb.Company')),
                ('production_countries', models.ManyToManyField(related_name='_movie_production_countries_+', to='moviedb.Country')),
                ('spoken_languages', models.ManyToManyField(related_name='_movie_spoken_languages_+', to='moviedb.Language')),
            ],
            managers=[
                ('initialize', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Network',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headquarters', models.CharField(max_length=1024, null=True)),
                ('homepage', models.CharField(max_length=255, null=True)),
                ('name', models.CharField(max_length=2048, null=True)),
                ('origin_country', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='moviedb.Country', to_field='iso_3166_1')),
            ],
            bases=(models.Model, moviedb.models.TmdbInitMixin),
            managers=[
                ('initialize', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birthday', models.DateField(null=True)),
                ('known_for_department', models.CharField(max_length=32)),
                ('deathday', models.DateField(null=True)),
                ('name', models.CharField(max_length=32)),
                ('also_known_as', models.CharField(blank=True, max_length=2048, null=True)),
                ('gender', models.IntegerField(default=0)),
                ('biography', models.TextField()),
                ('popularity', models.FloatField(default=0)),
                ('place_of_birth', models.CharField(max_length=64, null=True)),
                ('profile_path', models.CharField(max_length=64, null=True)),
                ('adult', models.BooleanField(default=False)),
                ('imdb_id', models.CharField(max_length=16)),
                ('homepage', models.URLField(null=True)),
            ],
            bases=(models.Model, moviedb.models.TmdbInitMixin),
            managers=[
                ('initialize', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, unique=True)),
                ('url', models.URLField(max_length=1024)),
            ],
            managers=[
                ('initialize', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='TvEpisode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('air_date', models.DateField(null=True)),
                ('series_id', models.IntegerField(default=0)),
                ('episode_number', models.IntegerField(default=0)),
                ('name', models.CharField(default='no_name', max_length=2024)),
                ('overview', models.TextField(blank=True, null=True)),
                ('production_code', models.CharField(blank=True, max_length=128, null=True)),
                ('season_number', models.IntegerField(default=0)),
                ('still_path', models.CharField(max_length=64, null=True)),
                ('vote_average', models.FloatField(default=0)),
                ('vote_count', models.IntegerField(default=0)),
                ('crew', models.ManyToManyField(related_name='_tvepisode_crew_+', to='moviedb.Person')),
                ('guest_stars', models.ManyToManyField(related_name='_tvepisode_guest_stars_+', to='moviedb.Person')),
            ],
            managers=[
                ('initialize', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='TvSeason',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_id', models.CharField(default='', max_length=32, unique=True)),
                ('air_date', models.DateField(null=True)),
                ('name', models.CharField(default='', max_length=1024)),
                ('overview', models.TextField(blank=True, null=True)),
                ('season_number', models.IntegerField(default=0)),
                ('episodes', models.ManyToManyField(to='moviedb.TvEpisode')),
            ],
            managers=[
                ('initialize', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='TvSeries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('backdrop_path', models.CharField(max_length=64, null=True)),
                ('episode_run_time', models.CharField(default='', max_length=514)),
                ('first_air_date', models.DateField(null=True)),
                ('homepage', models.URLField(null=True)),
                ('in_production', models.BooleanField(default=False)),
                ('last_air_date', models.DateField(null=True)),
                ('name', models.CharField(default='', max_length=1024)),
                ('number_of_episodes', models.IntegerField(default=0)),
                ('number_of_seasons', models.IntegerField(default=0)),
                ('origin_country', models.CharField(max_length=512)),
                ('original_name', models.CharField(default='', max_length=1024)),
                ('overview', models.TextField(null=True)),
                ('popularity', models.FloatField(default=0)),
                ('poster_path', models.CharField(max_length=64, null=True)),
                ('status', models.CharField(default='', max_length=16)),
                ('type', models.CharField(default='', max_length=16)),
                ('vote_average', models.FloatField(default=0)),
                ('vote_count', models.IntegerField(default=0)),
                ('created_by', models.ManyToManyField(to='moviedb.Person')),
                ('genres', models.ManyToManyField(to='moviedb.Genre')),
                ('languages', models.ManyToManyField(related_name='_tvseries_languages_+', to='moviedb.Language')),
                ('last_episode_to_air', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='last_episode_to_air+', to='moviedb.TvEpisode')),
                ('networks', models.ManyToManyField(to='moviedb.Network')),
                ('next_episode_to_air', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='next_episode_to_air+', to='moviedb.TvEpisode')),
                ('original_language', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='moviedb.Language')),
                ('production_companies', models.ManyToManyField(related_name='_tvseries_production_companies_+', to='moviedb.Company')),
                ('seasons', models.ManyToManyField(to='moviedb.TvSeason')),
            ],
            managers=[
                ('initialize', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.CharField(max_length=32, primary_key=True, serialize=False, unique=True)),
                ('key', models.CharField(max_length=64, null=True)),
                ('name', models.CharField(max_length=128, null=True)),
                ('size', models.IntegerField(choices=[(360, 360), (480, 480), (720, 720), (1080, 1080)], default=360)),
                ('type', models.CharField(choices=[('No Description', 'No Description'), ('Trailer', 'Trailer'), ('Teaser', 'Teaser'), ('Clip', 'Clip'), ('Behind the Scenes', 'Behind the Scenes'), ('Bloopers', 'Bloopers')], default='No Description', max_length=24)),
                ('note', models.TextField(blank=True, null=True)),
                ('iso_3166_1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moviedb.Country')),
                ('iso_639_1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moviedb.Language', to_field='iso_639_1')),
                ('movie', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='movie+', to='moviedb.Movie')),
                ('site', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='moviedb.Site', to_field='name')),
                ('tv_series', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tv_series+', to='moviedb.TvSeries')),
            ],
            managers=[
                ('movie_initialize', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='ExternalID',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imdb_id', models.CharField(max_length=9, null=True)),
                ('facebook_id', models.CharField(max_length=64, null=True)),
                ('instagram_id', models.CharField(max_length=64, null=True)),
                ('twitter_id', models.CharField(max_length=64, null=True)),
                ('movie_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moviedb.Movie')),
                ('tv_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moviedb.TvSeries')),
            ],
        ),
        migrations.CreateModel(
            name='Credit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cast', models.ManyToManyField(related_name='_credit_cast_+', to='moviedb.Person')),
                ('crew', models.ManyToManyField(related_name='_credit_crew_+', to='moviedb.Person')),
                ('movie', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='moviedb.Movie')),
                ('tv_series', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='moviedb.TvSeries')),
            ],
            managers=[
                ('movie_initialize', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='company',
            name='origin_country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='moviedb.Country', to_field='iso_3166_1'),
        ),
        migrations.AddField(
            model_name='company',
            name='parent_company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='moviedb.Company'),
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024)),
                ('overview', models.TextField()),
                ('poster_path', models.CharField(max_length=255, null=True)),
                ('backdrop_path', models.CharField(max_length=255, null=True)),
                ('parts', models.ManyToManyField(to='moviedb.Movie')),
            ],
            managers=[
                ('initialize', django.db.models.manager.Manager()),
            ],
        ),
    ]
