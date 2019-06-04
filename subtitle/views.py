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
        movie = tmdbsimple.Movies(id=self.kwargs['id'])

        context['movie'] = movie.info()
        context['persons'] = movie.credits()
        context['videos'] = movie.videos()
        context['similar'] = movie.similar_movies()
        context['keywords'] = movie.keywords()
        return context


class TvDetail(generic.ListView):
    model = Subtitle

    def get_queryset(self, **kwargs):
        query = super(TvDetail, self).get_queryset()

        return query


class Search(generic.TemplateView):
    template_name = 'search.html'
