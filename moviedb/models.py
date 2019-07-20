import datetime
import json
import os
from time import sleep

import colorama
import tmdbsimple
from django.conf import settings
from django.db import models
# Create your models here.
from django.template.defaultfilters import truncatechars
from django.utils.safestring import mark_safe
from requests import HTTPError


class TmdbInitMixin:
    def __init__(self):
        colorama.init()
        self.NO_DATA_ID = 9999999
        self.tmdb = tmdbsimple
        self.tmdb.API_KEY = settings.TMDB_API_KEY
        base_url = settings.TMDB_IMAGE_BASE['base_url']
        self.poster_url = base_url + '/{poster_size}'.format(poster_size=settings.TMDB_POSTER_SIZE['w154'])
        self.backdrop_url = base_url + '/{backdrop_size}'.format(backdrop_size=settings.TMDB_BACKDROP_SIZE['w300'])
        self.logo_url = base_url + '/{logo_size}'.format(logo_size=settings.TMDB_LOGO_SIZE['w154'])
        self.profile_url = base_url + '/{profile_size}'.format(profile_size=settings.TMDB_PROFILE_SIZE['w185'])
        self.stil_url = base_url + '/{still_size}'.format(still_size=settings.TMDB_STIL_SIZE['w185'])


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


class LanguageManager(models.Manager, TmdbInitMixin):
    def check_language(self, iso_639_1):
        try:
            obj = Language.initialize.get(iso_639_1=iso_639_1)
        except Language.DoesNotExist:
            obj = None
        return obj

    def initialize_data(self):
        with open(os.path.join(settings.BASE_DIR, 'dataset/initialize_data/language.json'), encoding='UTF-8') as f:
            for idx, line in enumerate(f):
                data = json.loads(line)
                obj, created = self.get_or_create(iso_639_1=data['iso_639_1'], defaults=data)
                if created:
                    print("country {}-{}({}) been added".format(obj.iso_639_1, obj.english_name, obj.name))
        print('language initialize complete')
        return True


class Language(models.Model):
    iso_639_1 = models.CharField(max_length=64, unique=True)
    english_name = models.CharField(max_length=64)
    name = models.CharField(max_length=64, default='unknown')
    initialize = LanguageManager()

    def __str__(self):
        return "{}[{}]".format(self.english_name, self.name)


class CountryManager(models.Manager, TmdbInitMixin):

    def initialize_data(self):
        with open(os.path.join(settings.BASE_DIR, 'dataset/initialize_data/country.json'), encoding='UTF-8') as f:
            for idx, line in enumerate(f):
                data = json.loads(line)
                self.get_or_create_country(
                    country_id=data['id'], iso_3166_1=data['iso_3166_1'], english_name=data['english_name'])
        print('country initialize complete')
        return True

    def check_country(self, iso_3166_1):
        try:
            obj = Country.initialize.get(iso_3166_1=iso_3166_1)
        except Country.DoesNotExist:
            obj = None

        return obj

    def get_or_create_country(self, country_id=0, iso_3166_1=0, english_name=""):
        if self.check_country(iso_3166_1):
            return self.get(iso_3166_1=iso_3166_1)
        else:
            obj = self.create(
                id=country_id,
                iso_3166_1=iso_3166_1,
                english_name=english_name
            )
            print("country {}-{} been added".format(obj.iso_3166_1, obj.english_name))
            return obj


class Country(models.Model):
    iso_3166_1 = models.CharField(max_length=2, unique=True)
    english_name = models.CharField(max_length=16, default='unknown')
    note = models.CharField(max_length=1024, null=True, blank=True)
    initialize = CountryManager()

    def __str__(self):
        return "[{}]{}".format(self.iso_3166_1, self.english_name)


class GenreManager(models.Manager, TmdbInitMixin):

    def initialize_data(self):

        genres = self.tmdb.Genres()
        movie_genres = genres.movie_list()
        tv_genres = genres.tv_list()

        for genre in movie_genres['genres']:
            g_obj, created = self.get_or_create(id=genre['id'], name=genre['name'])
            if created:
                print("Genre {}:{} added".format(g_obj.id, g_obj.name))
            else:
                print("Genre {}:{} exists".format(g_obj.id, g_obj.name))
        for genre in tv_genres['genres']:
            g_obj, created = self.get_or_create(id=genre['id'], name=genre['name'])
            if created:
                print("Genre {}:{} added".format(g_obj.id, g_obj.name))
            else:
                print("Genre {}:{} exists".format(g_obj.id, g_obj.name))
        print('genre initialize complete')
        return True

    def check_genre(self, genre_id):
        return self.get(id=genre_id)

    def get_or_create_genre(self, genre_id, genre_name):
        if self.check_genre(genre_id):
            obj = self.get(id=genre_id)
            print('genre {}-{} is already exist'.format(obj.id, obj.name))
        else:
            obj = self.create(id=genre_id, name=genre_name)
            print('genre {}-{} added'.format(obj.id, obj.name))
        return obj


class Genre(models.Model, TmdbInitMixin):
    name = models.CharField(max_length=32, default='unknown')
    initialize = GenreManager()

    def __str__(self):
        return self.name


class CompanyManager(models.Manager, TmdbInitMixin):

    def check_company(self, company_id):
        return self.filter(id=company_id).exists()

    def get_company(self, company_id):
        if self.check_company(company_id):
            return self.get(id=company_id)
        else:
            return None

    def get_or_create_company(self, company_id):
        if self.check_company(company_id):
            obj = self.get(id=company_id)
            print('company {}-{} is already exist'.format(obj.id, obj.name))
            return obj
        else:
            try:
                data = self.tmdb.Companies(company_id).info()
            except HTTPError:
                obj = self.get(id=self.NO_DATA_ID)
                obj.description = obj.description + ',' + str(company_id)
                obj.save()
                print(colorama.Back.RED + 'id {} company doesn\'t exist'.format(company_id) + colorama.Style.RESET_ALL)
                return obj
            # check parent company first
            if data['parent_company'] is not None:
                parent = self.get_company(data['parent_company']['id'])
                if parent is None:
                    parent = self.get_or_create_company(data['parent_company']['id'])
            else:
                parent = None
            # check country obj
            if data['origin_country'] is not None:
                origin_country = Country.initialize.check_country(iso_3166_1=data['origin_country'])
                if origin_country is None:
                    origin_country = Country.initialize.get(id=self.NO_DATA_ID)
            else:
                origin_country = Country.initialize.get(id=self.NO_DATA_ID)
            obj = self.create(
                id=data['id'],
                headquarters=data['headquarters'],
                homepage=data['homepage'],
                logo_path=data['logo_path'],
                name=data['name'],
                origin_country=origin_country,
                parent_company=parent
            )
            print(colorama.Fore.BLUE +
                  'comapny {}-{} been added'
                  .format(obj.id, obj.name) +
                  colorama.Style.RESET_ALL)
            return obj


class Company(models.Model, TmdbInitMixin):
    description = models.TextField(null=True, default="")
    headquarters = models.CharField(max_length=255, default="")
    homepage = models.URLField(null=True)
    logo_path = models.CharField(max_length=64, null=True)
    name = models.CharField(max_length=1024, default="unknown")
    origin_country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, to_field='iso_3166_1')
    parent_company = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    initialize = CompanyManager()

    def logo(self):
        if self.logo_path:
            path = settings.TMDB_IMAGE_BASE['base_url'] + settings.TMDB_LOGO_SIZE['w45'] + self.logo_path
        else:
            path = "https://via.placeholder.com/45?text=no+logo"
        img = u"<img src='{path}' alt={alt}/>".format(path=path, alt=self.name)
        return mark_safe(img)

    def __str__(self):
        return self.name


class KeywordManager(models.Manager, TmdbInitMixin):

    def initialize_data(self):
        with open(os.path.join(settings.BASE_DIR, 'dataset/initialize_data/keyword.json'), encoding='UTF-8') as f:
            for idx, line in enumerate(f):
                data = json.loads(line)

                if self.check_keyword(data['id']):
                    obj = self.get(id=data['id'])
                    print('{}-keyword {}:{} exist'.format(idx, obj.id, obj.name))
                else:
                    obj = self.create(**data)
                    print(colorama.Fore.MAGENTA +
                          '{}-keyword {}:{} added'.format(idx, obj.id, obj.name) +
                          colorama.Style.RESET_ALL)
            print('keyword initialize complete')
        return True

    def check_keyword(self, keyword_id):
        try:
            obj = Keyword.initialize.get(id=keyword_id)
        except Keyword.DoesNotExist:
            obj = None
        return obj

    def get_or_create_keyword(self, keyword_id, keyword_name):
        obj = self.check_keyword(keyword_id)
        if obj is not None:
            print(colorama.Fore.MAGENTA +
                  'keyword {}:{} exists'.format(obj.id, obj.name) +
                  colorama.Style.RESET_ALL)
            return obj
        obj = self.create(id=keyword_id, name=keyword_name)
        print(colorama.Fore.MAGENTA +
              'keyword {}:{} added'.format(obj.id, obj.name) +
              colorama.Style.RESET_ALL)
        return obj


class Keyword(models.Model):
    name = models.CharField(max_length=128, default='unknown')
    initialize = KeywordManager()

    def __str__(self):
        return self.name


class MovieManager(models.Manager, TmdbInitMixin):

    def check_movie(self, movie_id):
        try:
            obj = Movie.initialize.get(id=movie_id)
        except Movie.DoesNotExist:
            obj = None
        return obj

    def get_or_create_movie(self, movie_id):
        obj = self.check_movie(movie_id)
        if obj:
            return obj
        try:
            data = self.tmdb.Movies(movie_id).info()
        except HTTPError:
            obj = self.get(id=self.NO_DATA_ID)
            obj.overview = obj.overview + ',' + str(movie_id)
            print(colorama.Back.RED + "movie {} is not in API" + colorama.Style.RESET_ALL)
            return obj
        obj = self.create(
            id=data['id'],
            adult=data['adult'],
            backdrop_path=data['backdrop_path'],
            budget=data['budget'],
            homepage=data['homepage'],
            imdb_id=data['imdb_id'],
            original_language=Language.initialize.get(iso_639_1=data['original_language']),
            original_title=data['original_title'],
            overview=data['overview'],
            popularity=data['popularity'],
            poster_path=data['poster_path'],
            release_date=validate_date_format(data['release_date']),
            revenue=data['revenue'],
            runtime=data['runtime'],
            status=data['status'],
            tagline=data['tagline'],
            title=data['title'],
            video=data['video'],
            vote_average=data['vote_average'],
            vote_count=data['vote_count']
        )

        genres = data['genres']
        keyword_data = self.tmdb.Movies(movie_id).keywords()
        keywords = keyword_data['keywords']
        production_companies = data['production_companies']
        production_countries = data['production_countries']
        spoken_languages = data['spoken_languages']

        for genre in genres:
            g_obj = Genre.initialize.get_or_create_genre(genre_id=genre['id'], genre_name=genre['name'])
            obj.genres.add(g_obj)
        for keyword in keywords:
            k_obj = Keyword.initialize.get_or_create_keyword(keyword_id=keyword['id'],
                                                             keyword_name=keyword['name'])
            obj.keyword.add(k_obj)
        for production_company in production_companies:
            pc_obj = Company.initialize.get_or_create_company(company_id=production_company['id'])
            obj.production_companies.add(pc_obj)
        for production_country in production_countries:
            py_obj = Country.initialize.check_country(iso_3166_1=production_country['iso_3166_1'])
            obj.production_countries.add(py_obj)
        for spoken_language in spoken_languages:
            s_obj = Language.initialize.check_language(iso_639_1=spoken_language['iso_639_1'])
            obj.spoken_languages.add(s_obj)
        obj.save()
        print(
            colorama.Back.BLUE + colorama.Fore.BLACK +
            'movie id: {} title: {}({}) added'
            .format(obj.id, obj.title, obj.original_title) + colorama.Style.RESET_ALL)

        sleep(0.8)
        return obj

    def initialize_data(self):
        with open(os.path.join(settings.BASE_DIR, 'dataset/initialize_data/movie.json'), encoding='UTF-8') as f:
            for idx, line in enumerate(f):
                m_json = json.loads(line)

                if self.check_movie(m_json['id']):
                    print(colorama.Fore.WHITE + 'movie {}-{}:{} exists'.format(
                        obj.id, obj.title, obj.original_title) + colorama.Style.RESET_ALL)
                else:
                    obj = self.get_or_create_movie(m_json['id'])
        return True


class Movie(models.Model):
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
    keyword = models.ManyToManyField(Keyword, related_name='keyword+')
    original_language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True, to_field='iso_639_1')
    original_title = models.CharField(max_length=1024, default="No Original Title")
    overview = models.TextField(null=True)
    popularity = models.FloatField(default=0)
    poster_path = models.CharField(max_length=128, null=True)
    production_companies = models.ManyToManyField(Company, related_name='production_companies+')
    production_countries = models.ManyToManyField(Country, related_name='production_countries+')
    release_date = models.DateField(null=True)
    revenue = models.BigIntegerField(default=0)
    runtime = models.IntegerField(null=True)
    spoken_languages = models.ManyToManyField(Language, related_name='spoken_language+')
    status = models.CharField(max_length=32, choices=STATUS, default="Canceled")
    tagline = models.CharField(max_length=2048, null=True)
    title = models.CharField(max_length=1024, default="unknown")
    video = models.BooleanField(default=False)
    vote_average = models.FloatField(default=0)
    vote_count = models.IntegerField(default=0)
    initialize = MovieManager()

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


class PersonManager(models.Manager, TmdbInitMixin):

    def check_person(self, person_id):
        try:
            obj = Person.initialize.get(id=person_id)
        except Person.DoesNotExist:
            obj = None
        return obj

    @staticmethod
    def set_aka(obj, name):
        if obj.also_known_as:
            obj.also_known_as = obj.also_known_as + ',' + name
        else:
            obj.also_known_as = name
        return obj

    def get_or_create_person(self, person_id):
        obj = self.check_person(person_id=person_id)
        if obj is not None:
            return obj
        try:
            data = self.tmdb.People(person_id).info()
        except HTTPError:
            print(colorama.Back.RED + 'person {} does not exist in API ' + colorama.Style.RESET_ALL)
            obj = self.get(id=self.NO_DATA_ID)
            obj.biography = obj.biography + ',' + str(person_id)
            obj.save()
            return obj
        obj = self.create(
            id=data['id'],
            birthday=validate_date_format(data['birthday']),
            known_for_department=data['known_for_department'],
            deathday=validate_date_format(data['deathday']),
            name=data['name'],
            gender=data['gender'],
            biography=data['biography'],
            popularity=data['popularity'],
            place_of_birth=data['place_of_birth'],
            profile_path=data['profile_path'],
            adult=data['adult'],
            imdb_id=data['imdb_id'],
            homepage=data['homepage']
        )
        for aka in data['also_known_as']:
            obj = self.set_aka(obj, aka)
        obj.save()
        print(colorama.Fore.MAGENTA + "{}-{} been added".format(obj.id, obj.name))
        return obj

    def initialize_data(self):
        if not self.check_person(self.NO_DATA_ID):
            self.create(
                id=self.NO_DATA_ID,
                known_for_department='unknown',
                name='unknown',
                imdb_id='tt99999',
            )
        with open(os.path.join(settings.BASE_DIR, 'dataset/initialize_data/person.json'), encoding='UTF-8') as f:
            for idx, line in enumerate(f):
                p_json = json.loads(line)

                if self.check_person(p_json['id']):
                    obj = self.get(id=p_json['id'])
                    print(colorama.Fore.WHITE + 'person {}-{} exists'.format(
                        obj.id, obj.name) + colorama.Style.RESET_ALL)
                else:
                    self.get_or_create_person(p_json['id'])
        return True


class Person(models.Model, TmdbInitMixin):
    birthday = models.DateField(null=True)
    known_for_department = models.CharField(max_length=32, default='unknown')
    deathday = models.DateField(null=True)
    name = models.CharField(max_length=32, default='unknown')
    also_known_as = models.CharField(max_length=2048, null=True, blank=True)
    gender = models.IntegerField(default=0)
    biography = models.TextField(null=True, blank=True)
    popularity = models.FloatField(default=0)
    place_of_birth = models.CharField(max_length=64, null=True)
    profile_path = models.CharField(max_length=64, null=True)
    adult = models.BooleanField(default=False)
    imdb_id = models.CharField(max_length=16)
    homepage = models.URLField(null=True)
    initialize = PersonManager()

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


class SiteManager(models.Manager, TmdbInitMixin):

    def initialize_data(self):
        with open(os.path.join(settings.BASE_DIR, 'dataset/initialize_data/site.json'), encoding='UTF-8') as f:
            for idx, line in enumerate(f):
                s_json = json.loads(line)
                self.create(*s_json)
            print('Site Initialize Complete')
            return True


class Site(models.Model):
    name = models.CharField(max_length=16, unique=True)
    url = models.URLField(max_length=1024)
    initialize = SiteManager()

    def __str__(self):
        return self.name


class NetworkManager(models.Manager, TmdbInitMixin):

    def check_network(self, network_id):
        return self.get(id=network_id)

    def get_or_create_network(self, network_id):
        obj = self.check_network(network_id)
        if obj is not None:
            return obj

        try:
            data = self.tmdb.Networks(network_id).info()
        except HTTPError:
            obj = self.get(id=self.NO_DATA_ID)
            obj.headquarters = obj.headquarters + ',' + str(network_id)
            obj.save()
            print(colorama.Back.RED +
                  'Network {}-{} is not exist in API data'
                  .format(obj.id, obj.name) + colorama.Style.RESET_ALL)
            return obj

        obj = self.create(
            id=data['id'],
            headquarters=data['headquarters'],
            homepage=data['homepage'],
            name=data['name'],
            origin_country=Country.objects.get(iso_3166_1=data['origin_country'])
        )

        print(colorama.Fore.MAGENTA +
              '{}-{} network been added'.format(obj.id, obj.name) +
              colorama.Style.RESET_ALL)
        return obj

    def initialize_data(self):

        with open(os.path.join(settings.BASE_DIR, 'dataset/initialize_data/network.json'), encoding='UTF-8') as f:
            for idx, line in enumerate(f):
                n_json = json.loads(line)

                if self.check_network(n_json['id']):
                    obj = self.get(id=n_json['id'])
                    print(
                        colorama.Back.RED + 'network {}-{} exists'.format(obj.id, obj.name) + colorama.Style.RESET_ALL)
                else:
                    self.get_or_create_network(n_json['id'])
        return True


class Network(models.Model, TmdbInitMixin):
    headquarters = models.CharField(max_length=1024, null=True)
    homepage = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=2048, default='unknown')
    origin_country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, to_field='iso_3166_1')
    initialize = NetworkManager()

    def __str__(self):
        return '{}-{}'.format(self.name, self.headquarters)


class TvEpisodeManger(models.Manager, TmdbInitMixin):

    def get_or_create_episode(self, series_id, season_number, episode_number):
        obj = self.get(series_id, season_number, episode_number)
        if obj is not None:
            return obj
        try:
            data = self.tmdb.TV_Episodes(series_id, season_number, episode_number).info()
        except HTTPError:
            print(colorama.Back.RED + 'series_{} season{} episode {} is not in API'
                  .format(series_id, season_number, episode_number) + colorama.Style.RESET_ALL)
            obj = self.get(id=self.NO_DATA_ID)
            obj.overview = obj.overview + ',' + os.path.join(str(series_id), [str(season_number), str(episode_number)])
            obj.save()
            return obj

        obj = self.create(
            id=data['id'],
            air_date=validate_date_format(data['air_date']),
            episode_number=data['episode_number'],
            name=data['name'],
            overview=data['overview'],
            production_code=data['production_code'],
            season_number=season_number,
            still_path=data['still_path'],
            vote_average=data['vote_average'],
            vote_count=data['vote_count']
        )
        crews = data['crew']
        guest_stars = data['guest_stars']

        for crew in crews:
            c_obj = Person.initialize.get_or_create_person(person_id=crew['id'])
            obj.crew.add(c_obj)
        for stars in guest_stars:
            s_obj = Person.initialize.get_or_create_person(person_id=stars['id'])
            obj.guest_stars.add(s_obj)
        obj.save()
        print(colorama.Fore.GREEN +
              '{}:{} season_{} episode_{} been added'
              .format(obj.id, obj.name, obj.season_number, obj.episode_number)
              + colorama.Style.RESET_ALL
              )
        return obj


class TvEpisode(models.Model):
    air_date = models.DateField(null=True)
    crew = models.ManyToManyField(Person, related_name='crew+')
    series_id = models.IntegerField(default=0)
    episode_number = models.IntegerField(default=0)
    guest_stars = models.ManyToManyField(Person, related_name='stars+')
    name = models.CharField(max_length=2024, default="unknown")
    overview = models.TextField(null=True, blank=True)
    production_code = models.CharField(null=True, max_length=128, blank=True)
    season_number = models.IntegerField(default=0)
    still_path = models.CharField(max_length=64, null=True)
    vote_average = models.FloatField(default=0)
    vote_count = models.IntegerField(default=0)
    initialize = TvEpisodeManger()

    def __str__(self):
        return '{}-{}-{}'.format(self.name, self.season_number, self.episode_number)


class TvSeasonManager(models.Manager, TmdbInitMixin):

    def check_season(self, series_id, season_number):
        return self.get(series_id, season_number)

    def get_or_create_season(self, series_id, season_number):
        obj = self.check_season(series_id, season_number)
        if obj is not None:
            return obj
        try:
            data = self.tmdb.TV_Seasons(series_id, season_number).info()
        except HTTPError:
            obj = self.get(id=self.NO_DATA_ID)
            obj.overview = obj.overview + ',' + os.path.join(str(series_id), str(season_number))
            obj.save()
            print(colorama.Back.RED + 'Tv Series_{} season_{} is not in API'
                  .format(series_id, season_number) + colorama.Style.RESET_ALL)
            return obj
        obj = self.create(
            id=data['id'],
            _id=data['_id'],
            air_date=validate_date_format(data['air_date']),
            name=data['name'],
            overview=data['overview'],
            season_number=data['season_number'],
        )
        episodes = data['episodes']

        for episode in episodes:
            e_obj = TvEpisode.initialize.get_or_create_episode(series_id=series_id, season_number=season_number,
                                                               episode_number=episode['episode_number'])
            obj.episodes.add(e_obj)
        obj.save()
        print(colorama.Fore.GREEN + "tv season {}:{}-season_{} been added"
              .format(obj.id,
                      obj.name,
                      obj.season_number) + colorama.Style.RESET_ALL)

        return obj


class TvSeason(models.Model):
    _id = models.CharField(max_length=32, default="", unique=True)
    air_date = models.DateField(null=True)
    episodes = models.ManyToManyField(TvEpisode)
    name = models.CharField(max_length=1024, default="unknown")
    overview = models.TextField(blank=True, null=True)
    season_number = models.IntegerField(default=0)
    initialize = TvSeasonManager()

    def __str__(self):
        return '{}-{}[season_number_{}]'.format(self.id, self.name, self.season_number)


class TvSeriesManager(models.Manager, TmdbInitMixin):

    def check_tv_series(self, series_id):
        return self.get(id=series_id)

    def get_or_create_tv_series(self, series_id):
        obj = self.check_tv_series(series_id)
        if obj is not None:
            return obj
        try:
            data = self.tmdb.TV(series_id).info()
        except HTTPError:
            obj = self.get(id=self.NO_DATA_ID)
            obj.overview = obj.overview + ',' + str(series_id)
            obj.save()
            print(colorama.Back.RED + 'tv series {} is not in API'.format(series_id) + colorama.Style.RESET_ALL)
            return obj

        if data['last_episode_to_air']:
            last_episode_to_air = TvEpisode.initialize.get_or_create_episode(
                series_id=series_id,
                season_number=data['last_episode_to_air']['season_number'],
                episode_number=data['last_episode_to_air']['episode_number']
            )
        else:
            last_episode_to_air = None

        if data['next_episode_to_air']:
            next_episode_to_air = TvEpisode.initialize.get_or_create_episode(
                series_id=series_id,
                season_number=data['next_episode_to_air']['season_number'],
                episode_number=data['next_episode_to_air']['episode_number']
            )
        else:
            next_episode_to_air = None
        obj = self.create(
            id=series_id,
            backdrop_path=data['backdrop_path'],
            first_air_date=validate_date_format(data['first_air_date']),
            homepage=data['homepage'],
            in_production=data['in_production'],
            last_air_date=validate_date_format(data['last_air_date']),
            last_episode_to_air=last_episode_to_air,
            name=data['name'],
            next_episode_to_air=next_episode_to_air,
            number_of_episodes=data['number_of_episodes'],
            number_of_seasons=data['number_of_seasons'],
            original_name=data['original_name'],
            overview=data['overview'],
            popularity=data['popularity'],
            poster_path=data['poster_path'],
            status=data['status'],
            type=data['type'],
            vote_average=data['vote_average'],
            vote_count=data['vote_count']
        )
        created_by = data['created_by']
        for runtime in data['episode_run_time']:
            obj.episode_run_time = self.set_run_time(obj, runtime)
        genres = data['genres']
        languages = data['languages']
        networks = data['networks']
        origin_country = data['origin_country']
        production_companies = data['production_companies']
        seasons = data['seasons']

        for person in created_by:
            p_obj = Person.initialize.get_or_create(person['id'])
            obj.created_by.add(p_obj)
        for genre in genres:
            g_obj = Genre.initialize.get_or_create_genre(genre_id=genre['id'], genre_name=genre['name'])
            obj.genres.add(g_obj)
        for language in languages:
            l_obj = Language.objects.get(iso_639_1=language['iso_639_1'])
            obj.languages.add(l_obj)
        for network in networks:
            n_obj = Network.initialize.get_or_create_network(network['id'])
            obj.networks.add(n_obj)
        for country in origin_country:
            c_obj = Country.objects.get(iso_3166_1=country['id'])
            obj.origin_country = c_obj
        for production_company in production_companies:
            pc_obj = Company.initialize.get_or_create_company(production_company['id'])
            obj.production_companies.add(pc_obj)
        for season in seasons:
            s_obj = TvSeason.initialize.get_or_create_season(series_id=series_id, season_number=season['season_number'])
            obj.seasons.add(s_obj)
        obj.save()
        print(colorama.Back.BLUE + colorama.Fore.GREEN + 'Tv Show: {}-{} on air {} to {} added'
              .format(obj.id, obj.name, obj.first_air_date,
                      obj.last_air_date) + colorama.Style.RESET_ALL)
        return obj

    @staticmethod
    def set_runtime(obj, runtime):
        if obj.episode_run_time:
            obj.episode_run_time = obj.episode_run_time + ',' + str(runtime)
        else:
            obj.episode_run_time = str(runtime)
        return obj

    def initialize_data(self):
        if not self.get(id=self.NO_DATA_ID):
            self.create(
                id=self.NO_DATA_ID,
                name='No Series',
            )
        with open(os.path.join(settings.BASE_DIR, 'dataset/tv_series.json'), encoding='UTF-8') as f:
            for idx, line in enumerate(f):
                t_json = json.loads(line)

                try:
                    data = self.tmdb.TV(t_json['id']).info()
                except HTTPError:
                    obj = self.get(id=self.NO_DATA_ID)
                    obj.overview = obj.overview + ',' + str(data['id'])
                    print(colorama.Back.RED + 'Tv Series {} is not in API' + colorama.Style.RESET_ALL)
                    continue
                self.get_or_create_tv_series(data['id'])

            print("Tv Series Initialize complete")


class TvSeries(models.Model):
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
    name = models.CharField(max_length=1024, default="unknown")
    networks = models.ManyToManyField(Network)
    next_episode_to_air = models.ForeignKey(TvEpisode, on_delete=models.CASCADE, null=True,
                                            related_name='next_episode_to_air+')
    number_of_episodes = models.IntegerField(default=0)
    number_of_seasons = models.IntegerField(default=0)
    origin_country = models.CharField(max_length=512)
    original_language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True)
    original_name = models.CharField(max_length=1024, default="unknown")
    overview = models.TextField(null=True)
    popularity = models.FloatField(default=0)
    poster_path = models.CharField(max_length=64, null=True)
    production_companies = models.ManyToManyField(Company, related_name='production_companies+')
    seasons = models.ManyToManyField(TvSeason)
    status = models.CharField(max_length=16, default="")
    type = models.CharField(max_length=16, default="")
    vote_average = models.FloatField(default=0)
    vote_count = models.IntegerField(default=0)
    initialize = TvSeriesManager()

    def __str__(self):
        if self.name == self.original_name:
            return self.name
        else:
            return '{}({})'.format(self.name, self.original_name)

    def get_run_time(self):
        if self.episode_run_time:
            return self.episode_run_time.split(',')
        else:
            return None

    def get_origin_country(self):
        if self.origin_country:
            return self.origin_country.split(',')
        else:
            return None


class VideoManager(models.Manager, TmdbInitMixin):
    def initialize_data(self):
        if self.get(self.NO_DATA_ID):
            self.create(
                id=self.NO_DATA_ID,
                name="no video"
            )
            return True
        return False


class MovieVideoManager(VideoManager, TmdbInitMixin):
    @staticmethod
    def check_video(movie_id):
        try:
            obj = Videos.movie_initialize.filter(movie=Movie.initialize.get_or_create_movie(movie_id))
        except Videos.DoesNotExist:
            obj = None
        return obj

    def add_video(self, data):

        obj = self.create(
            id=data['id'],
            iso_639_1=Language.initialize.get(iso_639_1=data['iso_639_1']),
            iso_3166_1=Country.initialize.get(iso_3166_1=data['iso_3166_1']),
            key=data['key'],
            name=data['name'],
            site=Site.objects.get(name=data['site']),
            size=data['size'],
            type=data['type']
        )
        return obj

    def get_or_create_video(self, movie_id):
        obj = self.check_video(movie_id)
        if obj is not None:
            return obj
        try:
            data = self.tmdb.Movies(movie_id).videos()
        except HTTPError:
            obj = self.get(id=self.NO_DATA_ID)
            obj.note = obj.note + ',' + str(movie_id)
            obj.save()
            print(colorama.Back.RED + 'video for movie {} is not in API'.format(movie_id) + colorama.Style.RESET_ALL)
            return obj

        obj = self.create(
            movie=Movie.initialize.get_or_create_movie(movie_id)
        )
        for video in data['results']:
            v_obj = self.add_video(video)
            obj.videos.add(v_obj)
            print(colorama.Back.BLUE + colorama.Fore.GREEN + 'Movie Video: {}-[{}]{} added'
                  .format(v_obj.id, v_obj.type, v_obj.name) + colorama.Style.RESET_ALL)
        obj.save()
        return obj


class TvVideoManager(VideoManager, TmdbInitMixin):
    def check_vide(self, series_id):
        return self.get(tv_series=TvSeries.initialize.get_or_create_tv_series(series_id))

    def get_or_create_video(self, series_id):
        obj = self.check_video(series_id)
        if obj is not None:
            return obj
        try:
            data = self.tmdb.TV(series_id).videos()
        except HTTPError:
            obj = self.get(id=self.NO_DATA_ID)
            obj.note = obj.note + ',' + str(series_id)
            obj.save()
            print(colorama.Back.RED + 'movie {} is not in API'.format(series_id) + colorama.Style.RESET_ALL)
            return obj

        obj = self.create(
            id=data['id'],
            iso_639_1=Language.objects.get(iso_639_1=data['iso_639_1']),
            iso_3166_1=Country.objects.get(iso_3166_1=data['iso_3166_1']),
            key=data['key'],
            name=data['name'],
            site=Site.objects.get(name=data['site']),
            size=data['size'],
            type=data['type']
        )
        print(colorama.Back.BLUE + colorama.Fore.GREEN + 'Tv Video: {}-[{}]{} added'
              .format(obj.id, obj.type, obj.name) + colorama.Style.RESET_ALL)
        return obj


class Video(models.Model):
    SIZE = [
        (360, 360),
        (480, 480),
        (720, 720),
        (1080, 1080)
    ]
    TYPE = [
        ("No Description", "No Description"),
        ("Trailer", "Trailer",),
        ("Teaser", "Teaser",),
        ("Clip", "Clip"),
        ("Behind the Scenes", "Behind the Scenes"),
        ("Bloopers", "Bloopers")
    ]

    id = models.CharField(max_length=32, unique=True, primary_key=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True, related_name='movie+')
    tv_series = models.ForeignKey(TvSeries, on_delete=models.CASCADE, null=True, related_name='tv_series+')
    iso_639_1 = models.ForeignKey(Language, on_delete=models.CASCADE, to_field='iso_639_1', null=True)
    iso_3166_1 = models.ForeignKey(Country, on_delete=models.CASCADE, to_field='iso_3166_1', null=True)
    key = models.CharField(max_length=64, null=True)
    name = models.CharField(max_length=128, default='unknown')
    site = models.ForeignKey(Site, on_delete=models.CASCADE, to_field='name', null=True)
    size = models.IntegerField(choices=SIZE, default=360)
    type = models.CharField(max_length=24, choices=TYPE, default='No Description')
    note = models.TextField(null=True, blank=True)


class Videos(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True, related_name='movie+')
    tv_series = models.ForeignKey(TvSeries, on_delete=models.CASCADE, null=True, related_name='tv_series+')
    videos = models.ManyToManyField(Video, related_name='vidoes+')
    note = models.TextField(null=True, blank=True)
    movie_initialize = MovieVideoManager()
    tv_initialize = TvVideoManager()


class ExternalID(models.Model):
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    tv_id = models.ForeignKey(TvSeries, on_delete=models.CASCADE)
    imdb_id = models.CharField(max_length=9, null=True)
    facebook_id = models.CharField(max_length=64, null=True)
    instagram_id = models.CharField(max_length=64, null=True)
    twitter_id = models.CharField(max_length=64, null=True)


class MovieCreditManager(models.Manager, TmdbInitMixin):
    def check_credit(self, movie_id):
        try:
            obj = Credit.movie_initialize.get(movie=Movie.initialize.get_or_create_movie(movie_id))
        except Credit.DoesNotExist:
            obj = None
        return obj

    def update_or_create_credit(self, movie_id):
        obj = self.check_credit(movie_id)
        if obj:
            return obj
        data = self.tmdb.Movies(movie_id).credits()

        obj = self.create(
            movie=Movie.initialize.get_or_create_movie(movie_id=data['id'])
        )
        for cast in data['cast']:
            c_obj = Person.initialize.get_or_create_person(cast['id'])
            obj.cast.add(c_obj)
        for crew in data['crew']:
            c_obj = Person.initialize.get_or_create_person(crew['id'])
            obj.crew.add(c_obj)
        obj.save()
        print(colorama.Fore.BLUE + 'Movie Credit for {} added'.format(obj.movie.title) + colorama.Style.RESET_ALL)
        return obj


class TvCreditManager(models.Manager, TmdbInitMixin):
    def check_credit(self, movie_id):
        return self.get(
            movie=Movie.initialize.get_or_create_movie(movie_id)
        )

    def update_or_create(self, series_id):
        obj = self.check_credit(series_id)
        if obj:
            return obj
        data = self.tmdb.TV(series_id).credits()

        obj = self.create(
            tv_series=TvSeries.initialize.get_or_create_movie(data['id'])
        )
        for cast in data['cast']:
            c_obj = Person.initialize.get_or_create_person(cast['id'])
            obj.cast.add(c_obj)
        for crew in data['crew']:
            c_obj = Person.initialize.get_or_create_person(crew['id'])
            obj.crew.add(c_obj)
        obj.save()
        print(colorama.Fore.BLUE + 'Tv Series Credit for {} added'.format(obj.movie.title) + colorama.Style.RESET_ALL)
        return obj


class Credit(models.Model):
    movie = models.OneToOneField(Movie, on_delete=models.CASCADE, null=True)
    tv_series = models.OneToOneField(TvSeries, on_delete=models.CASCADE, null=True)
    cast = models.ManyToManyField(Person, related_name='cast+')
    crew = models.ManyToManyField(Person, related_name='crew+')
    movie_initialize = MovieCreditManager()
    tv_initialize = TvCreditManager()


class CollectionManager(models.Manager, TmdbInitMixin):
    def check_collection(self, collection_id):
        try:
            obj = Collection.initialize.get(id=collection_id)
        except Collection.DoesNotExist:
            obj = None
        return obj

    def get_or_create_collection(self, collection_id):
        obj = self.check_collection(collection_id)
        if obj:
            return obj
        try:
            data = self.tmdb.Collections(collection_id).info()
        except HTTPError:
            obj = self.get(id=self.NO_DATA_ID)
            obj.overview = obj.overview + ',' + str(collection_id)
            return obj
        obj = self.create(
            id=data['id'],
            name=data['name'],
            overview=data['overview'],
            poster_path=data['poster_path'],
            backdrop_path=data['backdrop_path']
        )

        for part in data['parts']:
            p_obj = Movie.initialize.get_or_create_movie(movie_id=part['id'])
            obj.parts.add(p_obj)
        obj.save()
        print(
            colorama.Back.BLUE + colorama.Fore.BLACK +
            'movie id: {} title: {} added'
            .format(obj.id, obj.name) + colorama.Style.RESET_ALL)

        sleep(0.8)
        return obj

    def initialize_data(self):
        with open(os.path.join(settings.BASE_DIR, 'dataset/initialize_data/collection.json'), encoding='UTF-8') as f:
            for idx, line in enumerate(f):
                m_json = json.loads(line)
                obj = self.check_collection(m_json['id'])
                if obj:
                    print(colorama.Fore.WHITE + 'collection {}-{} exists'.format(
                        obj.id, obj.name) + colorama.Style.RESET_ALL)
                else:
                    self.get_or_create_collection(m_json['id'])
        return True


class Collection(models.Model):
    name = models.CharField(max_length=1024, default='unknown')
    overview = models.TextField()
    poster_path = models.CharField(max_length=255, null=True)
    backdrop_path = models.CharField(max_length=255, null=True)
    parts = models.ManyToManyField(Movie)
    initialize = CollectionManager()

    def __str__(self):
        return self.name
