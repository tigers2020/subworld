from django.views.generic import TemplateView
from tmdbv3api import TMDb, Movie, Genre
from . import settings

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        tmdb = TMDb()
        tmdb.api_key = settings.TMDB_API_KEY

        tmdb.language = 'en'
        tmdb.debug = True

        movie = Movie()
        popular = movie.search('성난 황소')
        genre = Genre()
        nowplaying = movie.now_playing()
        context['populars'] = popular
        context['genre'] = genre
        context['nowplaying'] = nowplaying

        return context