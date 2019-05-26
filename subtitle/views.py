# Create your views here.
import tmdbsimple
from django.conf import settings
from django.views import generic

from subtitle.models import Subtitle


class MovieDetail(generic.ListView):
    model = Subtitle

    def get_context_data(self, *args, **kwargs):
        context = super(MovieDetail, self).get_context_data(*args, **kwargs)
        tmdbsimple.API_KEY = settings.TMDB_API_KEY


        print(context)
        movie = tmdbsimple.Movies(id=self.kwargs['id']).info()


        context['movie'] = movie

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

