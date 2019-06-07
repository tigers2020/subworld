# Create your views here.
import tmdbsimple
from django.conf import settings
from django.views import generic

from subtitle.models import Subtitle
from django.contrib.auth.models import AnonymousUser


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


class UploadView(generic.CreateView):
    model = Subtitle
    fields = ['user', 'title', 'sub_file', 'language', 'resolution', 'rip', 'comment']

    def get_context_data(self, **kwargs):
        context = super(UploadView, self).get_context_data(**kwargs)

        if self.request.GET:
            tmdbsimple.API_KEY = settings.TMDB_API_KEY
            context['movie'] = tmdbsimple.Movies(self.request.GET.get('movie_id')).info()

            context['image_url'] = settings.TMDB_IMAGE_BASE
            context['poster_size'] = settings.TMDB_POSTER_SIZE
            return context

        return context
