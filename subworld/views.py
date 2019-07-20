import tmdbsimple
from django.views.generic import TemplateView

from moviedb.models import Movie, TvSeries
from subtitle.models import MovieSubtitleInfo
from subworld.Paginator import Paginator
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
        subtitle = MovieSubtitleInfo.objects.all().order_by('-upload_date')[:20]

        movie = self.tmdb.Movies()
        page = self.request.GET.get('page', 1)

        populars = movie.popular(page=page)
        for m_data in populars['results']:
            id = m_data['id']
            Movie.initialize.get_or_create_movie(movie_id=id)

        nowplaying = movie.now_playing()
        for m_data in nowplaying['results']:
            id = m_data['id']
            Movie.initialize.get_or_create_movie(movie_id=id)
        keywords = []
        for now in populars['results'][:3]:
            keywords.append(self.tmdb.Movies(now['id']).keywords())
        #
        # for info in populars['results']:
        #     create_update_db(Movie, info)
        # for info in nowplaying['results']:
        #     create_update_db(Movie, info)
        paginator = Paginator(object_lists=populars['results'], total_pages=populars['total_pages'],
                              total_results=populars['total_results']).get_page(page)

        context['subtitles'] = subtitle
        context['populars'] = populars
        context['keywords'] = keywords
        context['nowplaying'] = nowplaying['results'][:6]
        context['paginator'] = paginator
        return context


class MovieIndexView(BaseSetMixin, TemplateView):
    template_name = 'movie_index.html'
    locator = 'movie_index'

    def get_context_data(self, **kwargs):
        context = super(MovieIndexView, self).get_context_data(**kwargs)
        subtitle = MovieSubtitleInfo.objects.all()[:20]

        movie = self.tmdb.Movies()
        page = self.request.GET.get('page', 1)

        popular = movie.popular(page=page)

        paginator = Paginator(object_lists=popular['results'], total_results=popular['total_results'],
                              total_pages=popular['total_pages']).get_page(page)

        context['paginator'] = paginator
        context['populars'] = popular['results']
        context['subtitles'] = subtitle

        return context


class TvShowIndexView(BaseSetMixin, TemplateView):
    template_name = 'tv_show_index.html'
    locator = 'tv_show_index'

    def get_context_data(self, **kwargs):
        context = super(TvShowIndexView, self).get_context_data(**kwargs)
        subtitle = MovieSubtitleInfo.objects.all()[:20]

        tv_show = self.tmdb.TV()
        page = self.request.GET.get('page', 1)

        popular = tv_show.popular(page=page)
        on_the_air = tv_show.on_the_air(page=page)
        for info in popular['results']:
            create_update_db(TvSeries, info)
        for info in on_the_air['results']:
            create_update_db(TvSeries, info)
        paginator = Paginator(object_lists=popular['results'], total_results=popular['total_results'],
                              total_pages=popular['total_pages']).get_page(page)

        context['paginator'] = paginator
        context['populars'] = popular['results']
        context['subtitles'] = subtitle

        return context




def create_update_db(db, data):
    info, created = db.objects.update_or_create(id=data['id'], defaults=data)
    if created:
        print("create {}".format(info))
    else:
        print("update {}".format(info))


def check_movie_new_db(db, data):
    if data['result']:
        for info in data['results']:
            print("create/update: ", info['title'])
            db.objects.update_or_create(id=info['id'], defaults=info)

def check_tv_new_db(db, data):
    for info in data['results']:
        print("create/update: ", info['name'])
        db.objects.update_or_create(id=info['id'],
                                    defaults=info)
