from django.shortcuts import render
from django.views.generic import TemplateView
import tmdbsimple
from . import settings


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        tmdbsimple.API_KEY = settings.TMDB_API_KEY

        movie = tmdbsimple.Movies()
        movie.popular()
        genre = tmdbsimple.Genres()

        nowplaying = tmdbsimple.Movies().now_playing()
        context['populars'] = movie
        context['genre'] = genre.movie_list()
        context['nowplaying'] = nowplaying['results'][:8]

        return context


def search(request):
    if request.GET:
        s = request.GET.get('search')
        try:
            t = request.GET.get('type')
        except:
            t = None
        tmdb = TMDb()
        tmdb.api_key = settings.TMDB_API_KEY

        if t == "movie":
            movie = Movie().search(s)
            context = {'movies': movie, 's': s}
            template = 'search/search_movie.html'
            return render(request, template, context)
        elif t == "person":
            people = Person().search(s)
            context = {'person': people, 's': s}
            template = 'search/search_person.html'
            return render(request, template, context)
        elif t == "tv_show":
            tv_show = TV().search(s)
            context = {'tv_show': tv_show, 's': s}
            template = 'search/search_tv_show.html'
            return render(request, template, context)
        else:
            context = {}
            template = "search_failed.html"
            return render(request, template, context)
