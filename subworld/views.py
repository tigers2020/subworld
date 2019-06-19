import tmdbsimple
from django.views.generic import TemplateView

from search.models import MovieDB, TvSeriesDB
from subtitle.models import MovieSubtitle
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
        subtitle = MovieSubtitle.objects.all().order_by('-upload_date')[:20]

        movie = self.tmdb.Movies()
        page = self.request.GET.get('page', 1)

        populars = movie.popular(page=page)
        nowplaying = movie.now_playing()
        keywords = []
        for now in populars['results'][:3]:
            keywords.append(tmdbsimple.Movies(now['id']).keywords())

        check_new_db(MovieDB, populars)
        check_new_db(MovieDB, nowplaying)
        paginator = Paginator(object_lists=populars['results'], total_pages=populars['total_pages'],
                              total_results=populars['total_results']).get_page(page)

        context['subtitles'] = subtitle
        context['populars'] = populars
        context['keywords'] = keywords
        context['nowplaying'] = nowplaying['results'][:8]
        context['paginator'] = paginator
        return context


class MovieIndexView(BaseSetMixin, TemplateView):
    template_name = 'movie_index.html'
    locator = 'movie_index'

    def get_context_data(self, **kwargs):
        context = super(MovieIndexView, self).get_context_data(**kwargs)
        subtitle = MovieSubtitle.objects.all()[:20]

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
        subtitle = MovieSubtitle.objects.all()[:20]

        tv_show = self.tmdb.TV()
        page = self.request.GET.get('page', 1)

        popular = tv_show.popular(page=page)
        on_the_air = tv_show.on_the_air(page=page)
        check_new_db(TvSeriesDB, popular)
        check_new_db(TvSeriesDB, on_the_air)
        paginator = Paginator(object_lists=popular['results'], total_results=popular['total_results'],
                              total_pages=popular['total_pages']).get_page(page)

        context['paginator'] = paginator
        context['populars'] = popular['results']
        context['subtitles'] = subtitle

        return context


def check_new_db(db, data):
    for info in data['results']:
        print("create/update: ", info['title'])
        db.objects.update_or_create(id=info['id'],
                                    defaults=info)
