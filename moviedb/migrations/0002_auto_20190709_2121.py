# Generated by Django 2.2.1 on 2019-07-10 01:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('moviedb', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Credit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cast', models.ManyToManyField(related_name='_credit_cast_+', to='moviedb.Person')),
                ('crew', models.ManyToManyField(related_name='_credit_crew_+', to='moviedb.Person')),
                ('movie_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='moviedb.Movie')),
                ('tv_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='moviedb.Tv')),
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
                ('tv_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moviedb.Tv')),
            ],
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.RemoveField(
            model_name='movieexternalid',
            name='movie_id',
        ),
        migrations.RemoveField(
            model_name='moviekeyword',
            name='movie_id',
        ),
        migrations.DeleteModel(
            name='MovieCredit',
        ),
        migrations.DeleteModel(
            name='MovieExternalID',
        ),
        migrations.DeleteModel(
            name='MovieKeyword',
        ),
    ]
