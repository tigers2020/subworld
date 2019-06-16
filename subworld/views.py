import json

import tmdbsimple
from django.views.generic import TemplateView

from search.models import MovieDB
from subtitle.models import Subtitle
from . import settings


class BaseSetMixin:
    locator = ''
    image_base = ""
    poster_size = ""
    backdrop_size = ""
    logo_size = ""
    profile_size = ""
    still_size = ""
    tmdb = ""

    def __init__(self):
        self.image_base = settings.TMDB_IMAGE_BASE
        self.poster_size = settings.TMDB_POSTER_SIZE
        self.backdrop_size = settings.TMDB_BACKDROP_SIZE
        self.logo_size = settings.TMDB_LOGO_SIZE
        self.profile_size = settings.TMDB_PROFILE_SIZE
        self.still_size = settings.TMDB_STIL_SIZE
        self.tmdb = tmdbsimple
        self.tmdb.API_KEY = settings.TMDB_API_KEY

    def get_context_data(self, **kwargs):
        context = super(BaseSetMixin, self).get_context_data(**kwargs)
        context['locator'] = self.locator
        context['image_base'] = self.image_base
        context['poster_size'] = self.poster_size
        context['backdrop_size'] = self.backdrop_size
        context['logo_size'] = self.logo_size
        context['profile_size'] = self.profile_size
        context['still_size'] = self.still_size
        return context


class IndexView(BaseSetMixin, TemplateView):
    template_name = 'index.html'
    locator = 'index'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        subtitle = Subtitle.objects.all().order_by('-upload_date')[:20]

        movie = self.tmdb.Movies()
        if self.request.GET:
            page = self.request.GET['page']
        else:
            page = 1
        populars = movie.popular(page=page)
        nowplaying = movie.now_playing()
        keywords = []
        for now in populars['results'][:3]:
            keywords.append(tmdbsimple.Movies(now['id']).keywords())

        check_new_db(MovieDB, populars)
        check_new_db(MovieDB, nowplaying)

        page_lead_in = int(page) - 5
        if page_lead_in <= 0:
            page_lead_in = 1
        page_lead_out = int(page) + 5
        if page_lead_out > populars['total_pages']:
            page_lead_out = populars['total_pages']

        context['subtitles'] = subtitle
        context['populars'] = populars
        context['keywords'] = keywords
        context['nowplaying'] = nowplaying['results'][:8]
        context['pop_pages'] = range(1, populars['total_pages'])
        context['page_lead_in'] = page_lead_in
        context['page_lead_out'] = page_lead_out

        # context['request'] = self.request
        return context


class MovieIndexView(BaseSetMixin, TemplateView):
    template_name = 'movie_index.html'
    locator = 'movie_index'


class TvShowIndexView(BaseSetMixin, TemplateView):
    template_name = 'tv_show_index.html'
    locator = 'tv_show_index'


def check_new_db(db, data):
    for info in data['results']:
        print("create/update: ", info['title'])
        db.objects.update_or_create(id=info['id'],
                                    defaults=info)


def check_db(db, data):
    with open(data, encoding="UTF-8") as f:
        for line in f:
            json_data = json.loads(line)
            if db.filter(id=json_data['id']):
                print("data exist", json_data)
            else:
                print("create", json_data)
                db.create(**json_data)

# class DbInit(TemplateView):
#     template_name = 'init.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(DbInit, self).get_context_data(**kwargs)
#
#         movie = models.MovieDB.objects.all()
#
#         collection = models.CollectionDB.objects.all()
#         tv_series = models.TvSeriesDB.objects.all()
#         production_company = models.ProductionCompanyDB.objects.all()
#         person = models.PersonDB.objects.all()
#         keyword = models.KeywordDB.objects.all()
#         tv_network = models.TvNetworkDB.objects.all()
#
#         check_data = {}
#
#         check_db(movie, "dataset/movie.json")
#         check_db(collection, "dataset/collection.json")
#         check_db(tv_series, "dataset/tv_series.json")
#         check_db(production_company, "dataset/production_company.json")
#         check_db(person, "dataset/person.json")
#         check_db(keyword, "dataset/keyword.json")
#         check_db(tv_network, "dataset/tv_network.json")
#
#         if movie:
#             check_data['movie'] = True
#         else:
#             check_data['movie'] = False
#
#         if collection:
#             check_data['collection'] = True
#         else:
#             check_data['collection'] = False
#         if tv_series:
#             check_data['tv_series'] = True
#         else:
#             check_data['tv_series'] = False
#         if production_company:
#             check_data['company'] = True
#         else:
#             check_data['company'] = False
#         if person:
#             check_data['person'] = True
#         else:
#             check_data['person'] = False
#         if keyword:
#             check_data['keyword'] = True
#         else:
#             check_data['keyword'] = False
#         if tv_network:
#             check_data['tv_network'] = True
#         else:
#             check_data['tv_network'] = False
#
#         context['check_data'] = check_data
#         context['movies'] = movie
#         context['collections'] = collection
#         context['tv_series'] = tv_series
#         context['production_companies'] = production_company
#         context['persons'] = person
#         context['keywords'] = keyword
#         context['tv_network'] = tv_network
#
#         return context
