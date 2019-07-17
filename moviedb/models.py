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
        colorama.init()
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
    return obj.objects.count() or 0


def validate_date_format(date_string):
    if date_string is not None:
        try:
            return datetime.datetime.strptime(date_string, "%Y-%m-%d")
        except ValueError:
            return None
    else:
        return None


def validate_int(number):
    if number is None:
        return 0
    elif number == "":
        return 0
    elif number > 0:
        return int(float(number))
    else:
        return 0


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
        return Country.objects.count()

    def get_count(self):
        return _get_count(self)


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
                genre = self.add_genre(data['id'], data['name'])
                print('{}-{} added'.format(genre.id, genre.name))
            for data in tv_genre['genres']:
                genre = self.add_genre(data['id'], data['name'])
                print('{}-{} added'.format(genre.id, genre.name))
        return Genre.objects.count()

    def add_genre(self, genre_id, name):
        try:
            genre, created = Genre.objects.get_or_create(genre_id, name)
            if created:
                genre.save()
                print("genre {}:{} added".format(genre.id, genre.name))
            return genre
        except IntegrityError:
            print('error')
            return None


class Company(models.Model, TmdbInitMixin):
    COMPANY_404 =[
        116703,
        84322,
        328,
        23335,
        2786,
    ]

    description = models.TextField(null=True, default="")
    headquarters = models.CharField(max_length=255, default="")
    homepage = models.URLField(null=True)
    logo_path = models.CharField(max_length=64, null=True)
    name = models.CharField(max_length=1024, default="")
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

    def add_company(self, company_id):
        company_id = validate_int(company_id)
        if company_id in Company.COMPANY_404:
            obj = Company.objects.get(id=999999)
            obj.description = '{},{}'.format(obj.description, str(company_id))
            obj.save()
            print(colorama.Back.RED + 'id {} company doesn\'t exist'.format(company_id) + colorama.Style.RESET_ALL)
            return obj
        try:
            company_info = self.tmdb.Companies(company_id).info()
        except HTTPError:
            obj = Company.objects.get(id=999999)
            obj.description = '{},{}'.format(obj.description, str(company_id))
            obj.save()
            print(colorama.Back.RED + 'id {} company doesn\'t exist'.format(company_id) + colorama.Style.RESET_ALL)
            return obj

        if company_info['origin_country']:
            origin_country = Country.objects.get(iso_3166_1=company_info['origin_country'])
        else:
            origin_country = Country.objects.get(iso_3166_1='XX')
        if company_info['parent_company']:
            try:
                parent_company = Company.objects.get(id=company_info['parent_company']['id'])
            except self.DoesNotExist:
                parent_company = Company().add_company(company_info['parent_company']['id'])
            except HTTPError:
                parent_company = Company.objects.get(id=999999)
        else:
            parent_company = Company.objects.get(id=999999)
        pc_obj = Company(
            id=company_info['id'],
            description=company_info['description'],
            headquarters=company_info['headquarters'],
            homepage=company_info['homepage'],
            logo_path=company_info['logo_path'],
            name=company_info['name'],
            origin_country=origin_country,
            parent_company=parent_company
        )
        pc_obj.save()

        print(colorama.Fore.BLUE +
              'comapny {}-{} been added'
              .format(pc_obj.id, pc_obj.name) +
              colorama.Style.RESET_ALL)

        return pc_obj


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
    budget = models.BigIntegerField(default=0)
    genres = models.ManyToManyField(Genre, related_name='genre+')
    homepage = models.URLField(null=True, max_length=2048)
    imdb_id = models.CharField(max_length=16, null=True)
    original_language = models.CharField(max_length=4, default="")
    original_title = models.CharField(max_length=1024, default="")
    overview = models.TextField(null=True)
    popularity = models.FloatField(default=0)
    poster_path = models.CharField(max_length=128, null=True)
    production_companies = models.ManyToManyField(Company, related_name='production_companies+')
    production_countries = models.ManyToManyField(Country, related_name='production_countries+')
    release_date = models.DateField(null=True)
    revenue = models.BigIntegerField(default=0)
    runtime = models.IntegerField(null=True)
    spoken_languages = models.ManyToManyField(Language, related_name='spoken_language+')
    status = models.CharField(max_length=32, choices=STATUS, default="")
    tagline = models.CharField(max_length=1024, null=True)
    title = models.CharField(max_length=1024, default="")
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

    def add_movie(self, idx, movie_id):
        try:
            movie_info = self.tmdb.Movies(movie_id).info()
        except HTTPError:
            return Movie.objects.get(id=1)
        obj = Movie(id=movie_id)
        # many to many field relate add
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
            obj.release_date = validate_date_format(movie_info['release_date'])
        obj.revenue = movie_info['revenue']
        obj.runtime = movie_info['runtime']
        obj.status = movie_info['status']
        obj.tagline = movie_info['tagline']
        obj.title = movie_info['title']
        obj.video = movie_info['video']
        obj.vote_average = movie_info['vote_average']
        obj.vote_count = movie_info['vote_count']
        obj.save()

        for genre in movie_info['genres']:
            try:
                genre_obj = Genre.objects.get(id=genre['id'])
            except Genre.DoesNotExist:
                genre_obj = Genre().add_genre(genre['id'], genre['name'])
            obj.genres.add(genre_obj)

        for production_country in movie_info['production_countries']:
            try:
                pc_obj = Country.objects.get(iso_3166_1=production_country['iso_3166_1'])
            except Country.DoesNotExist:
                pc_obj = Country.objects.get(iso_3166_1='XX')
            obj.production_countries.add(pc_obj)

        for production_company in movie_info['production_companies']:
            try:
                pc_obj = Company.objects.get(id=production_company['id'])
            except Company.DoesNotExist:
                pc_obj = Company().add_company(production_company['id'])
            except HTTPError:
                pc_obj = Company.objects.get(id=999999)
            obj.production_companies.add(pc_obj)
        obj.save()
        print(
            colorama.Back.BLUE + colorama.Fore.BLACK +
            '{}-create id: {} title: {}({})'
            .format(idx, obj.id, obj.title, obj.original_title) + colorama.Style.RESET_ALL)
        return obj

    def initiate_data(self):

        with open(os.path.join(settings.BASE_DIR, 'dataset/movie.json'), encoding='UTF-8') as f:
            for idx, line in enumerate(f):

                data = json.loads(line)
                movie_id = data['id']
                try:
                    obj = Movie.objects.get(id=movie_id)
                    print('{} - {}:{}({}) already exist'.format(idx, obj.id, obj.title, obj.original_title))
                except Movie.DoesNotExist:
                    obj = Movie().add_movie(idx, movie_id)

            return Movie.objects.count()


class Person(models.Model, TmdbInitMixin):
    birthday = models.DateField(null=True)
    known_for_department = models.CharField(max_length=32)
    deathday = models.DateField(null=True)
    name = models.CharField(max_length=32)
    also_known_as = models.CharField(max_length=2048)
    gender = models.IntegerField(default=0)
    biography = models.TextField()
    popularity = models.FloatField(default=0)
    place_of_birth = models.CharField(max_length=64, null=True)
    profile_path = models.CharField(max_length=64, null=True)
    adult = models.BooleanField(default=False)
    imdb_id = models.CharField(max_length=16)
    homepage = models.URLField(null=True)

    def set_aka(self, name):
        if self.also_known_as:
            self.also_known_as = self.also_known_as + ',' + name
        else:
            self.also_known_as = name

    def get_aka(self):
        if self.also_known_as:
            return self.also_known_as.split(",")
        else:
            return None

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

    def add_person(self, person_id):
        try:
            person = self.tmdb.People(person_id).info()
            obj = Person.objects.create(id=person_id)
            # check date valid
            birthday = validate_date_format(person['birthday'])
            deathday = validate_date_format(person['deathday'])
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
            for aka in person['also_known_as']:
                obj.set_aka(aka)
            obj.save()
            print('person {}:{} added'.format(obj.id, obj.name))
        except HTTPError:
            print("person {} does not exist in API data".format(person_id))
            obj = Person.objects.get(id=1)
        return obj

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
                    p_obj = self.add_person(person['id'])

                    if p_obj:
                        print(colorama.Fore.MAGENTA + "{}-{} been added".format(idx, p_obj.name))
                    sleep(0.5)
        return Person.objects.count()


class Keyword(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

    def get_count(self):
        return _get_count(self)

    def add_keyword(self, idx, data):
        obj = Keyword.objects.create(**data)
        print(colorama.Fore.MAGENTA +
              '{}-{}:{} added'.format(idx, obj.id, obj.name) +
              colorama.Style.RESET_ALL)
        return obj

    def initiate_data(self):
        with open(os.path.join(settings.BASE_DIR, 'dataset/keyword.json'), encoding='UTF-8') as f:
            for idx, line in enumerate(f):
                data = json.loads(line)
                k_id = data['id']
                try:
                    k_obj = Keyword.objects.get(id=k_id)
                    print('{}-{} exist'.format(idx, k_obj.name))
                except Keyword.DoesNotExist:
                    k_obj = Keyword().add_keyword(idx, data)
        return Keyword.objects.count()


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


class Network(models.Model, TmdbInitMixin):
    headquarters = models.CharField(max_length=1024)
    homepage = models.CharField(max_length=255)
    name = models.CharField(max_length=2048)
    origin_country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return '{}-{}'.format(self.name, self.headquarters)

    def get_count(self):
        return _get_count(self)

    def add_network(self, idx=0, network_id=0):
        tv_json = self.tmdb.Networks(network_id).info()
        if tv_json['origin_country'] is not "" or not None:
            origin_country = Country.objects.get(iso_3166_1=tv_json['origin_country'] or 'XX')
        else:
            print('country not exists')
            origin_country = Country.objects.get(iso_3166_1='XX')

        tv_obj = Network.objects.create(
            id=tv_json['id'],
            headquarters=tv_json['headquarters'],
            homepage=tv_json['homepage'],
            name=tv_json['name'],
            origin_country=origin_country
        )
        print(colorama.Fore.MAGENTA +
              '{}-{} network been added'.format(idx, tv_obj.name) +
              colorama.Style.RESET_ALL)
        return tv_obj

    def initiate_data(self):
        with open(os.path.join(settings.BASE_DIR, 'dataset/tv_network.json'), encoding='UTF-8') as f:
            for idx, line in enumerate(f):
                data = json.loads(line)
                tv_id = data['id']
                try:
                    obj = Network.objects.get(id=tv_id)
                    print('{}-{} network is exists'.format(idx, obj.name))

                except Network.DoesNotExist:
                    obj = Network().add_network(idx=idx, network_id=tv_id)

        return Network.objects.count()


class TvEpisode(models.Model, TmdbInitMixin):
    air_date = models.DateField(null=True)
    crew = models.ManyToManyField(Person, related_name='crew+')
    episode_number = models.IntegerField(default=0)
    guest_stars = models.ManyToManyField(Person, related_name='stars+')
    name = models.CharField(max_length=2024, default="no_name")
    overview = models.TextField(null=True, blank=True)
    production_code = models.CharField(null=True, max_length=128)
    season_number = models.IntegerField(default=0)
    still_path = models.CharField(max_length=64, null=True)
    vote_average = models.FloatField(default=0)
    vote_count = models.IntegerField(default=0)

    def get_count(self):
        return _get_count(self)

    def __str__(self):
        return '{}-{}-{}'.format(self.name, self.season_number, self.episode_number)

    def add_episode(self, series_id, season_number, episode_number):
        series_id = validate_int(series_id)
        season_number = validate_int(season_number)
        episode_number = validate_int(episode_number)

        tv_episode = self.tmdb.TV_Episodes(series_id, season_number, episode_number)
        ep_json = tv_episode.info()

        obj = TvEpisode.objects.create(id=ep_json['id'])
        obj.save()
        obj.air_date = validate_date_format(ep_json['air_date'])
        if ep_json['crew']:
            for crew in ep_json['crew']:
                if crew['id']:
                    print('crew id = ', crew['id'])
                    try:
                        c_obj = Person.objects.get(id=crew['id'])
                    except Person.DoesNotExist:
                        c_obj = Person().add_person(person_id=crew['id'])
                    obj.crew.add(c_obj)
        obj.episode_number = validate_int(ep_json['episode_number'])
        for guest_star in ep_json['guest_stars']:
            try:
                gs_obj = Person.objects.get(id=guest_star['id'])
            except Person.DoesNotExist:
                gs_obj = Person().add_person(person_id=guest_star['id'])
            obj.guest_stars.add(gs_obj)
        obj.name = ep_json['name']
        obj.overview = ep_json['overview']
        obj.production_code = ep_json['production_code']
        obj.season_number = ep_json['season_number']
        obj.still_path = ep_json['still_path']
        obj.vote_average = ep_json['vote_average']
        obj.vote_count = ep_json['vote_count']
        obj.save()
        print(colorama.Fore.GREEN +
              '{}:{} season_{} episode_{} been added'
              .format(obj.id, obj.name, obj.season_number, obj.episode_number)
              + colorama.Style.RESET_ALL
              )
        return obj


class TvSeason(models.Model, TmdbInitMixin):
    _id = models.CharField(max_length=32, default="")
    air_date = models.DateField(null=True)
    episodes = models.ManyToManyField(TvEpisode)
    name = models.CharField(max_length=1024, default="")
    overview = models.TextField(blank=True, null=True)
    season_number = models.IntegerField(default=0)

    def get_count(self):
        return _get_count(self)

    def __str__(self):
        return '{}-{}[season_number_{}]'.format(self.id, self.name, self.season_number)

    def add_season(self, series_id, season_number):
        series_id = validate_int(series_id)
        season_number = validate_int(season_number)
        s_json = self.tmdb.TV_Seasons(series_id, season_number).info()
        s_obj = TvSeason(s_json['id'])
        s_obj._id = s_json['_id']
        s_obj.air_date = validate_date_format(s_json['air_date'])
        s_obj.name = s_json['name']
        s_obj.overview = s_json['overview']
        s_obj.season_number = s_json['season_number']
        s_obj.save()
        # add episode
        for episode in s_json['episodes']:
            episode_number = validate_int(episode['episode_number'])
            try:
                e_obj = TvEpisode.objects.get(id=episode['id'])
                # check missing episode:

            except TvEpisode.DoesNotExist:
                e_obj = TvEpisode().add_episode(series_id, season_number, episode_number)
            except ValueError:
                print("value error at ")
                print('error: {}-{}-{}'.format(series_id, season_number, episode_number))
                e_obj = None
            s_obj.episodes.add(e_obj)
        s_obj.save()
        print(colorama.Fore.GREEN + "tv season {}:{}-season_{} been added".format(s_obj.id,
                                                                                  s_obj.name,
                                                                                  s_obj.season_number) + colorama.Style.RESET_ALL)
        return s_obj


class Tv(models.Model, TmdbInitMixin):
    backdrop_path = models.CharField(max_length=64, null=True)
    created_by = models.ManyToManyField(Person)
    episode_run_time = models.CharField(max_length=514, default="")
    first_air_date = models.DateField(null=True)
    genres = models.ManyToManyField(Genre)
    homepage = models.URLField(null=True)
    in_production = models.BooleanField(default=False)
    languages = models.ManyToManyField(Language, related_name='languages+')
    last_air_date = models.DateField(null=True)
    last_episode_to_air = models.ForeignKey(TvEpisode, on_delete=models.CASCADE, null=True,
                                            related_name='last_episode_to_air+')
    name = models.CharField(max_length=1024, default="")
    networks = models.ManyToManyField(Network)
    next_episode_to_air = models.ForeignKey(TvEpisode, on_delete=models.CASCADE, null=True,
                                            related_name='next_episode_to_air+')
    number_of_episodes = models.IntegerField(default=0)
    number_of_seasons = models.IntegerField(default=0)
    origin_country = models.CharField(max_length=512)
    original_language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True)
    original_name = models.CharField(max_length=1024, default="")
    overview = models.TextField(null=True)
    popularity = models.FloatField(default=0)
    poster_path = models.CharField(max_length=64, null=True)
    production_companies = models.ManyToManyField(Company, related_name='production_companies+')
    seasons = models.ManyToManyField(TvSeason)
    status = models.CharField(max_length=16, default="")
    type = models.CharField(max_length=16, default="")
    vote_average = models.FloatField(default=0)
    vote_count = models.IntegerField(default=0)

    def __str__(self):
        if self.name == self.original_name:
            return self.name
        else:
            return '{}({})'.format(self.name, self.original_name)

    def set_run_time(self, runtime):
        if self.episode_run_time:
            self.episode_run_time = self.episode_run_time + "," + str(runtime)
        else:
            self.episode_run_time = str(runtime)

    def get_run_time(self):
        if self.episode_run_time:
            return self.episode_run_time.split(',')
        else:
            return None

    def get_count(self):
        return _get_count(self)

    def initiate_data(self):
        with open(os.path.join(settings.BASE_DIR, 'dataset/tv_series.json'), encoding='UTF-8') as f:
            for idx, line in enumerate(f):
                data = json.loads(line)
                tv_id = int(data['id'])
                try:
                    tv_obj = Tv.objects.get(id=tv_id)
                    print('{}-{}:{}({}) show is exist'.format(idx, tv_obj.id, tv_obj.name, tv_obj.original_name))
                    # TODO: check missing seasons


                except Tv.DoesNotExist:
                    info = self.tmdb.TV(tv_id).info()
                    # save static data first
                    tv_obj = Tv(id=info['id'])
                    tv_obj.backdrop_path = info['backdrop_path']
                    tv_obj.first_air_date = validate_date_format(info['first_air_date'])
                    for episode_run_time in info['episode_run_time']:
                        tv_obj.set_run_time(episode_run_time)
                    for country in info['origin_country']:
                        tv_obj.set_origin_country(country)

                    tv_obj.homepage = info['homepage']
                    tv_obj.in_production = info['in_production']
                    last_air_date = validate_date_format(info['last_air_date'])
                    tv_obj.last_air_date = last_air_date
                    tv_obj.number_of_episodes = info['number_of_episodes']
                    tv_obj.number_of_seasons = info['number_of_seasons']
                    try:
                        original_language = Language.objects.get(iso_639_1=info['original_language'])
                    except Language.DoesNotExist:
                        original_language = Language.objects.get(iso_639_1='XX')
                    tv_obj.original_language = original_language
                    tv_obj.original_name = info['original_name']
                    tv_obj.overview = info['overview']
                    tv_obj.popularity = info['popularity']
                    tv_obj.poster_path = info['poster_path']
                    tv_obj.status = info['status']
                    tv_obj.type = info['type']
                    tv_obj.vote_average = info['vote_average']
                    tv_obj.vote_count = info['vote_count']
                    tv_obj.name = info['name']
                    tv_obj.save()

                    for person in info['created_by']:
                        try:
                            p_obj = Person.objects.get(id=person['id'])
                        except Person.DoesNotExist:
                            p_obj = Person().add_person(person_id=person['id'])
                        tv_obj.created_by.add(p_obj)
                    for language in info['languages']:
                        try:
                            lan_obj = Language.objects.get(iso_639_1=language)
                        except Language.DoesNotExist:
                            lan_obj = Language.objects.get(iso_639_1='XX')
                        tv_obj.languages.add(lan_obj)
                    for genre in info['genres']:
                        try:
                            g_obj = Genre.objects.get(id=genre['id'])
                        except Genre.DoesNotExist:
                            g_obj = Genre().add_genre(genre['id'], genre['name'])
                        tv_obj.genres.add(g_obj)
                    if info['last_episode_to_air']:
                        season_number = validate_int(info['last_episode_to_air']['season_number'])
                        episode_number = validate_int(info['last_episode_to_air']['episode_number'])
                        last_episode_to_air_id = validate_int(info['last_episode_to_air']['id'])
                        try:
                            last_episode_to_air = TvEpisode.objects.get(id=last_episode_to_air_id)
                        except TvEpisode.DoesNotExist:
                            last_episode_to_air = TvEpisode().add_episode(
                                tv_id,
                                season_number,
                                episode_number
                            )
                        tv_obj.last_episode_to_air = last_episode_to_air

                    if info['next_episode_to_air']:
                        try:
                            next_episode_to_air = TvEpisode.objects.get(id=info['next_episode_to_air']['id'])
                        except TvEpisode.DoesNotExist:
                            next_episode_to_air = TvEpisode().add_episode(
                                tv_id,
                                info['next_episode_to_air']['season_number'],
                                info['next_episode_to_air']['episode_number']
                            )
                        tv_obj.next_episode_to_air = next_episode_to_air
                    for network in info['networks']:
                        try:
                            n_obj = Network.objects.get(id=network['id'])
                        except Network.DoesNotExist:
                            n_obj = Network().add_network(network['id'])
                        tv_obj.networks.add(n_obj)

                    for p_company in info['production_companies']:
                        try:
                            p_obj = Company.objects.get(id=p_company['id'])
                        except Company.DoesNotExist:
                            p_obj = Company().add_company(p_company['id'])
                        tv_obj.production_companies.add(p_obj)
                    # add seasons
                    for season in info['seasons']:
                        try:
                            s_obj = TvSeason.objects.get(id=season['id'])
                        except TvSeason.DoesNotExist:
                            s_obj = TvSeason().add_season(tv_id, validate_int(season['season_number']))
                        tv_obj.seasons.add(s_obj)
                    tv_obj.save()
                    print(colorama.Back.BLUE + colorama.Fore.GREEN + 'Tv Show: {}-{} on air {} to {} added'
                          .format(tv_obj.id, tv_obj.name, tv_obj.first_air_date,
                                  tv_obj.last_air_date) + colorama.Style.RESET_ALL)
        return Tv.objects.count()

    def set_origin_country(self, country):
        if self.origin_country:
            self.origin_country = self.origin_country + ',' + country
        else:
            self.origin_country = country

    def get_origin_country(self):
        if self.origin_country:
            return self.origin_country.split(',')
        else:
            return None


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

class Collection(models.Model, TmdbInitMixin):
    name = models.CharField(max_length=1024)
    overview = models.TextField()
    poster_path = models.CharField(max_length=255, null=True)
    backdrop_path = models.CharField(max_length=255, null=True)
    parts = models.ManyToManyField(Movie)

    def __str__(self):
        return self.name

    def get_count(self):
        return _get_count(self)

    def initiate_data(self):
        with open(os.path.join(settings.BASE_DIR, 'dataset/collection.json'), encoding='UTF-8') as f:
            for idx, line in enumerate(f):

                data = json.loads(line)
                c_id = data['id']

                try:
                    obj = Collection.objects.get(id=c_id)
                    print('{}-{}:{} exists'.format(idx, obj.id, obj.name))
                except Collection.DoesNotExist:
                    try:
                        c_json = self.tmdb.Collections(c_id).info()
                    except HTTPError:
                        print(colorama.Back.RED + "{} does not exist".format(c_id) + colorama.Style.RESET_ALL)
                        continue

                    obj = Collection(
                        id=c_id,
                        name=c_json['name'],
                        poster_path=c_json['poster_path'],
                        backdrop_path=c_json['backdrop_path']
                    )
                    obj.save()
                    for movie in c_json['parts']:
                        try:
                            m_obj = Movie.objects.get(id=movie['id'])
                        except Movie.DoesNotExist:
                            m_obj = Movie().add_movie(idx=idx, movie_id=movie['id'])
                        obj.parts.add(m_obj)
                    obj.save()
                    print(colorama.Back.YELLOW + colorama.Fore.BLUE + '{} added'.format(obj.name) + colorama.Style.RESET_ALL)
        return Collection.objects.count()
