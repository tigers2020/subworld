import datetime
import json
import os
from time import sleep

import colorama
import tmdbsimple
from django.conf import settings
from django.db import models, IntegrityError
# Create your models here.
from django.template.defaultfilters import truncatechars
from django.utils.safestring import mark_safe
from requests import HTTPError


class TmdbInitMixin:
    def __init__(self):
        self.tmdb = tmdbsimple
        self.tmdb.API_KEY = settings.TMDB_API_KEY
        base_url = settings.TMDB_IMAGE_BASE['base_url']
        self.poster_url = base_url + '/{poster_size}'.format(poster_size=settings.TMDB_POSTER_SIZE['w154'])
        self.backdrop_url = base_url + '/{backdrop_size}'.format(backdrop_size=settings.TMDB_BACKDROP_SIZE['w300'])
        self.logo_url = base_url + '/{logo_size}'.format(logo_size=settings.TMDB_LOGO_SIZE['w154'])
        self.profile_url = base_url + '/{profile_size}'.format(profile_size=settings.TMDB_PROFILE_SIZE['w185'])
        self.stil_url = base_url + '/{still_size}'.format(still_size=settings.TMDB_STIL_SIZE['w185'])


def create_update_db(db, data):
    info, created = db.objects.update_or_create(id=data['id'], defaults=data)
    if created:
        print("create {}".format(info))
    else:
        print("update {}".format(info))


def _get_count(obj):
    return obj.objects.all().count() or 0


class Genre(models.Model, TmdbInitMixin):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

    def get_count(self):
        return _get_count(self)

    def initiate_data(self):
        if not Genre.objects.exists():
            genres = self.tmdb.Genres()
            movie_genre = genres.movie_list()
            tv_genre = genres.tv_list()
            for data in movie_genre['genres']:
                print('{} add'.format(data))
                Genre.objects.update_or_create(id=int(data['id']), name=data['name'])
            for data in tv_genre['genres']:
                print('{} add'.format(data))
                Genre.objects.update_or_create(id=int(data['id']), name=data['name'])
        return Genre.objects.all()


class Country(models.Model, TmdbInitMixin):
    iso_3166_1 = models.CharField(max_length=2, unique=True)
    english_name = models.CharField(max_length=16)

    def __str__(self):
        return "[{}]{}".format(self.iso_3166_1, self.english_name)

    def initiate_data(self):
        # if not Country.objects.exists():
        # import http.client
        #
        # conn = http.client.HTTPSConnection("api.themoviedb.org")
        #
        # payload = "{}"
        #
        # conn.request("GET", "/3/configuration/countries?api_key=c479f9ce20ccbcc06dbcce991a238120", payload)
        #
        # res = conn.getresponse()
        # data = res.read()
        # Country.objects.update_or_create(iso_3166_1=data['iso_3166_1'], english_name=data['english_name'] )
        return Country.objects.all()

    def get_count(self):
        return _get_count(self)


class Company(models.Model, TmdbInitMixin):
    description = models.TextField(null=True, default="")
    headquarters = models.CharField(max_length=255, default="")
    homepage = models.URLField(null=True)
    logo_path = models.CharField(max_length=64, null=True)
    name = models.CharField(max_length=32, default="")
    origin_country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)
    parent_company = models.ForeignKey('self', on_delete=models.CASCADE, null=True)

    def logo(self):
        if self.logo_path:
            path = settings.TMDB_IMAGE_BASE['base_url'] + settings.TMDB_LOGO_SIZE['w45'] + self.logo_path
        else:
            path = "https://via.placeholder.com/45?text=no+logo"
        img = u"<img src='{path}' alt={alt}/>".format(path=path, alt=self.name)
        return mark_safe(img)

    def __str__(self):
        return self.name

    def get_count(self):
        return _get_count(self)


class Language(models.Model):
    iso_639_1 = models.CharField(max_length=64, unique=True)
    english_name = models.CharField(max_length=64)
    name = models.CharField(max_length=64, null=True)

    def __str__(self):
        return "{}[{}]".format(self.english_name, self.name)

    def get_count(self):
        return _get_count(self)


class Movie(models.Model, TmdbInitMixin):
    STATUS = [
        ("Rumored", "Rumored"),
        ("Planned", "Planned"),
        ("InProduction", "In Production"),
        ("PostProduction", "Post Production"),
        ("Released", "Released"),
        ("Canceled", "Canceled")
    ]
    adult = models.BooleanField(default=False)
    backdrop_path = models.CharField(max_length=128, null=True, default="")
    budget = models.IntegerField(default=0)
    genres = models.ManyToManyField(Genre, related_name='genre+')
    homepage = models.URLField(null=True)
    imdb_id = models.CharField(max_length=9, null=True)
    original_language = models.CharField(max_length=4, default="")
    original_title = models.CharField(max_length=255, default="")
    overview = models.TextField(null=True)
    popularity = models.FloatField(default=0)
    poster_path = models.CharField(max_length=128, null=True)
    production_companies = models.ManyToManyField(Company, related_name='production_companies+')
    production_countries = models.ManyToManyField(Country, related_name='production_countries+')
    release_date = models.DateField(null=True)
    revenue = models.IntegerField(default=0)
    runtime = models.IntegerField(null=True)
    spoken_languages = models.ManyToManyField(Language, related_name='spoken_language+')
    status = models.CharField(max_length=32, choices=STATUS, default="")
    tagline = models.CharField(max_length=32, null=True)
    title = models.CharField(max_length=255, default="")
    video = models.BooleanField(default=False)
    vote_average = models.FloatField(default=0)
    vote_count = models.IntegerField(default=0)

    def poster(self):
        if self.poster_path:
            path = settings.TMDB_IMAGE_BASE['base_url'] + settings.TMDB_POSTER_SIZE['w92'] + self.poster_path
        else:
            path = "https://via.placeholder.com/45?text=no+poster"
        img = u"<img src='{path}' alt={alt}/>".format(path=path, alt=self.title)
        return mark_safe(img)

    def __str__(self):
        if self.title != self.original_title:
            return '{}({})'.format(self.original_title, self.title)
        else:
            return self.title

    def get_count(self):
        return _get_count(self)

    def initiate_data(self):
        colorama.init()
        with open(os.path.join(settings.BASE_DIR, 'dataset/movie.json'), encoding='UTF-8') as f:
            for idx, line in enumerate(f):

                data = json.loads(line)
                movie_id = data['id']
                try:
                    obj = Movie.objects.get(id=movie_id)
                    print('{} - {}:{}({}) already exist'.format(idx, obj.id, obj.title, obj.original_title))
                except Movie.DoesNotExist:
                    movie = self.tmdb.Movies(movie_id)
                    movie_info = movie.info()
                    print(colorama.Fore.GREEN + "{}-{}".format(idx, movie_info) + colorama.Style.RESET_ALL)
                    obj = Movie.objects.create(id=movie_id)
                    # many to many field relate add
                    for genre in movie_info['genres']:
                        genre_obj, created = Genre.objects.get_or_create(id=genre['id'], defaults=genre)
                        if created:
                            print("{}-{}".format(idx, genre))
                            print('{} genre {} been added'.format(genre_obj.id, genre_obj.name))
                        else:
                            print("{} genre {} already exist".format(genre_obj.id, genre_obj.name))
                        obj.genres.add(genre_obj)

                    for production_country in movie_info['production_countries']:
                        pc_obj, created = Country.objects.get_or_create(iso_3166_1=production_country['iso_3166_1'],
                                                                        defaults=production_country)
                        if created:
                            print("{}-{}".format(idx, pc_obj))
                            print("{} country been added".format(pc_obj.english_name))
                        else:
                            print("{} country is already exist".format(pc_obj.english_name))
                        obj.production_countries.add(pc_obj)

                    for production_company in movie_info['production_companies']:
                        try:
                            pc_obj = Company.objects.get(id=production_company['id'])
                            print("{} company already exists".format(pc_obj.name))
                        except Company.DoesNotExist:
                            try:
                                company_info = self.tmdb.Companies(production_company['id']).info()
                                pc_obj = Company(
                                    id=company_info['id'],
                                    description=company_info['description'],
                                    headquarters=company_info['headquarters'],
                                    homepage=company_info['homepage'],
                                    logo_path=company_info['logo_path'],
                                    name=company_info['name'],
                                    origin_country=Country.objects.get(
                                        iso_3166_1=company_info['origin_country']) or None
                                )
                                pc_obj.save()
                            except HTTPError:
                                pc_obj = None
                                continue
                            print(colorama.Fore.YELLOW + "{}-{} company been added".format(idx,
                                                                                           pc_obj.name) + colorama.Style.RESET_ALL)
                        obj.production_companies.add(pc_obj)

                    obj.adult = movie_info['adult']
                    obj.backdrop_path = movie_info['backdrop_path']
                    obj.budget = movie_info['budget']
                    obj.homepage = movie_info['homepage']
                    obj.imdb_id = movie_info['imdb_id']
                    obj.original_language = movie_info['original_language']
                    obj.original_title = movie_info['original_title']
                    obj.overview = movie_info['overview']
                    obj.popularity = movie_info['popularity']
                    obj.poster_path = movie_info['poster_path']
                    if movie_info['release_date'] != "":
                        obj.release_date = movie_info['release_date']
                    else:
                        obj.release_date = None
                    obj.revenue = movie_info['revenue']
                    obj.runtime = movie_info['runtime']
                    obj.status = movie_info['status']
                    obj.tagline = movie_info['tagline']
                    obj.title = movie_info['title']
                    obj.video = movie_info['video']
                    obj.vote_average = movie_info['vote_average']
                    obj.vote_count = movie_info['vote_count']
                    obj.save()
                    print(colorama.ansi.clear_screen())
                    print(
                        colorama.Back.BLUE + colorama.Fore.BLACK + '{}-create id: {} title: {}({})'.format(idx, obj.id,
                                                                                                           obj.title,
                                                                                                           obj.original_title) + colorama.Style.RESET_ALL)
                    sleep(0.8)
            return Movie.objects.all()


class AlsoKnownAs(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

    def get_count(self):
        return _get_count(self)


class Person(models.Model, TmdbInitMixin):
    birthday = models.DateField(null=True)
    known_for_department = models.CharField(max_length=32)
    deathday = models.DateField(null=True)
    name = models.CharField(max_length=32)
    also_known_as = models.ManyToManyField(AlsoKnownAs)
    gender = models.IntegerField(default=0)
    biography = models.TextField()
    popularity = models.FloatField(default=0)
    place_of_birth = models.CharField(max_length=64, null=True)
    profile_path = models.CharField(max_length=64, null=True)
    adult = models.BooleanField(default=False)
    imdb_id = models.CharField(max_length=9)
    homepage = models.URLField(null=True)

    def __str__(self):
        return self.name

    def profile(self):
        img = u"<img src='{path}' alt='{alt}' />"
        if self.profile_path:
            path = settings.TMDB_IMAGE_BASE['base_url'] + settings.TMDB_PROFILE_SIZE['w45'] + self.profile_path
            return mark_safe(img.format(path=path, alt=self.name))
        else:
            path = "https://via.placeholder.com/45?text=no+profile"
            return mark_safe(img.format(path=path, alt=self.name))

    def get_gender(self):
        switcher = {
            0: "Not set / not specified",
            1: "Female",
            2: "Male"
        }
        return switcher.get(self.gender, "")

    def short_biography(self):
        return truncatechars(self.biography, 150)

    def get_count(self):
        return _get_count(self)

    def initiate_data(self):
        with open(os.path.join(settings.BASE_DIR, 'dataset/person.json'), encoding='UTF-8') as f:
            for idx, line in enumerate(f):
                data = json.loads(line)
                p_id = data['id']
                try:
                    obj = Person.objects.get(id=p_id, name=data['name'])
                    print("{}: {} already exists".format(obj.id, obj.name))
                except Person.DoesNotExist:
                    person = self.tmdb.People(p_id).info()
                    print(person)
                    # check date valid
                    if person['birthday'] is not None:
                        try:
                            birthday = datetime.datetime.strptime(person['birthday'], "%Y-%m-%d")
                        except ValueError:
                            birthday = None
                    else:
                        birthday = None
                    if person['deathday'] is not None:
                        try:
                            deathday = datetime.datetime.strptime(person['deathday'], "%Y-%m-%d")
                        except ValueError:
                            deathday = None
                    else:
                        deathday = None

                    try:
                        obj = Person.objects.create(id=p_id)
                    except IntegrityError:
                        obj = Person.objects.get(id=p_id)
                    obj.save()
                    obj.name = person['name']
                    obj.birthday = birthday
                    obj.deathday = deathday
                    obj.gender = person['gender']
                    obj.biography = person['biography']
                    obj.popularity = person['popularity']
                    obj.place_of_birth = person['place_of_birth']
                    obj.profile_path = person['profile_path']
                    obj.adult = person['adult']
                    obj.imdb_id = person['imdb_id']
                    obj.homepage = person['homepage']

                    # add data into also known as and link it.
                    for aka in person['also_known_as']:
                        try:
                            aka_obj = AlsoKnownAs.objects.get(name=aka)
                        except AlsoKnownAs.DoesNotExist:
                            aka_obj = AlsoKnownAs(name=aka)
                            aka_obj.save()
                        obj.also_known_as.add(aka_obj)

                    obj.save()
                    sleep(0.5)
        return Person.objects.all()


class Keyword(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    def get_count(self):
        return _get_count(self)


class Site(models.Model):
    name = models.CharField(max_length=16)
    url = models.URLField()

    def __str__(self):
        return self.name

    def get_count(self):
        return _get_count(self)


class Videos(models.Model):
    SIZE = [
        ("360", "360"),
        ("480", "480"),
        ("720", "720"),
        ("1080", "1080")
    ]
    TYPE = [
        ("Trailer", "Trailer",),
        ("Teaser", "Teaser",),
        ("Clip", "Clip"),
        ("BehindTheScenes", "Behind the Scenes"),
        ("Bloopers", "Bloopers")
    ]
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    iso_639_1 = models.ForeignKey(Language, on_delete=models.CASCADE)
    iso_3166_1 = models.ForeignKey(Country, on_delete=models.CASCADE)
    key = models.CharField(max_length=64)
    name = models.CharField(max_length=128)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    size = models.IntegerField(choices=SIZE)
    type = models.CharField(max_length=16)

    def get_count(self):
        return _get_count(self)


class Network(models.Model):
    headquarters = models.CharField(max_length=64)
    homepage = models.CharField(max_length=128)
    name = models.CharField(max_length=64)
    origin_country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def get_count(self):
        return _get_count(self)


class TvEpisode(models.Model):
    air_date = models.DateField()
    crew = models.ManyToManyField(Person, related_name='crew+')
    episode_number = models.IntegerField()
    guest_stars = models.ManyToManyField(Person, related_name='stars+')
    name = models.CharField(max_length=32)
    overview = models.TextField()
    production_code = models.IntegerField()
    season_number = models.IntegerField()
    still_path = models.CharField(max_length=64, null=True)
    vote_average = models.FloatField()
    vote_count = models.IntegerField()

    def get_count(self):
        return _get_count(self)


class TvSeason(models.Model):
    _id = models.CharField(max_length=32)
    air_date = models.DateField()
    episodes = models.ManyToManyField(TvEpisode)
    name = models.CharField(max_length=16)
    overview = models.TextField(blank=True, null=True)
    poster_path = models.CharField(max_length=64)
    season_number = models.IntegerField()

    def get_count(self):
        return _get_count(self)


class Tv(models.Model):
    backdrop_path = models.CharField(max_length=64, null=True)
    created_by = models.ManyToManyField(Person)
    genres = models.ManyToManyField(Genre)
    homepage = models.URLField(null=True)
    in_production = models.BooleanField(default=False)
    languages = models.ManyToManyField(Language, related_name='languages+')
    last_air_date = models.DateField()
    last_episode_to_air = models.ForeignKey(TvEpisode, on_delete=models.CASCADE)
    Network = models.ManyToManyField(Network)
    number_of_episodes = models.IntegerField()
    number_of_seasons = models.IntegerField()
    origin_country = models.ManyToManyField(Country, related_name='origin_country+')
    original_language = models.ForeignKey(Language, on_delete=models.CASCADE)
    original_name = models.CharField(max_length=32)
    overview = models.TextField()
    popularity = models.FloatField()
    poster_path = models.CharField(max_length=64, null=True)
    production_companies = models.ManyToManyField(Company, related_name='production_companies+')
    seasons = models.ManyToManyField(TvSeason)
    status = models.CharField(max_length=16)
    type = models.CharField(max_length=16)
    vote_average = models.FloatField()
    vote_count = models.IntegerField()

    def get_count(self):
        return _get_count(self)


class ExternalID(models.Model):
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    tv_id = models.ForeignKey(Tv, on_delete=models.CASCADE)
    imdb_id = models.CharField(max_length=9, null=True)
    facebook_id = models.CharField(max_length=64, null=True)
    instagram_id = models.CharField(max_length=64, null=True)
    twitter_id = models.CharField(max_length=64, null=True)

    def get_count(self):
        return _get_count(self)


class Credit(models.Model):
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True)
    tv_id = models.ForeignKey(Tv, on_delete=models.CASCADE, null=True)
    cast = models.ManyToManyField(Person, related_name='cast+')
    crew = models.ManyToManyField(Person, related_name='crew+')

    def get_count(self):
        return _get_count(self)


# CONFIGURATION


class Job(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=32)

    def get_count(self):
        return _get_count(self)


class Jobs(models.Model):
    department = models.CharField(max_length=32)
    jobs = models.ManyToManyField(Job)

    def get_count(self):
        return _get_count(self)


class PrimaryTranslations(models.Model):
    name = models.CharField(max_length=5)

    def get_count(self):
        return _get_count(self)


class Region(models.Model):
    name = models.CharField(max_length=16)


class Zone(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    country = models.CharField(max_length=32)

    def __str__(self):
        return '{}/{}'.format(self.region, self.country)

    def get_count(self):
        return _get_count(self)


class TimeZone(models.Model):
    iso_3166_1 = models.ForeignKey(Country, on_delete=models.CASCADE)
    zones = models.ManyToManyField(Zone)

    def __str__(self):
        return self.iso_3166_1

    def get_count(self):
        return _get_count(self)


# END CONFIGURATION

# CERTIFICATION
class Certifications(models.Model):
    certification = models.CharField(max_length=6)
    meaning = models.TextField()
    order = models.IntegerField()

    def get_count(self):
        return _get_count(self)


class MovieCertifications(models.Model):
    region = models.ForeignKey(Country, on_delete=models.CASCADE)
    certifications = models.ManyToManyField(Certifications)

    def get_count(self):
        return _get_count(self)


class TVCertifications(models.Model):
    region = models.ForeignKey(Country, on_delete=models.CASCADE)
    certifications = models.ManyToManyField(Certifications)

    def get_count(self):
        return _get_count(self)


# END CERTIFICATION

class Collection(models.Model):
    name = models.CharField(max_length=128)
    overview = models.TextField()
    poster_path = models.CharField(max_length=255)
    backdrop_path = models.CharField(max_length=255)
    parts = models.ManyToManyField(Movie)

    def get_count(self):
        return _get_count(self)
