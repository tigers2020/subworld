# Create your views here.
import tmdbv3api
from django.conf import settings
from django.views import generic

from subtitle.models import Subtitle


class MovieDetail(generic.ListView):
    model = Subtitle

    def get_context_data(self, *args, **kwargs):
        context = super(MovieDetail, self).get_context_data(*args, **kwargs)

        tmdb = tmdbv3api.TMDb()
        tmdb.api_key = settings.TMDB_API_KEY
        print(context)
        detail = tmdbv3api.Movie().details(movie_id=280960)

        context['detail'] = detail

        return context

    def get_queryset(self, **kwargs):
        query = super(MovieDetail, self).get_queryset()
        return query


class TvDetail(generic.ListView):
    model = Subtitle

    def get_queryset(self, **kwargs):
        query = super(TvDetail, self).get_queryset()

        return query


class Search(generic.TemplateView):
    template_name = 'search.html'

