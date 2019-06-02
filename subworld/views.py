import tmdbsimple
from django.shortcuts import render
from django.views.generic import TemplateView

from . import settings


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        tmdbsimple.API_KEY = settings.TMDB_API_KEY

        movie = tmdbsimple.Movies()
        genre = tmdbsimple.Genres()
        page = 1
        if self.request.GET:
            page = self.request.GET['page']
        else:
            page = 1
        populars = movie.popular(page=page)

        page_lead_in = int(page) - 5
        if page_lead_in <= 0:
            page_lead_in = 1
        page_lead_out = int(page) + 5
        if page_lead_out > populars['total_pages']:
            page_lead_out = populars['total_pages']

        nowplaying = tmdbsimple.Movies().now_playing()
        keywords = []
        for now in nowplaying['results']:
            keywords.append(tmdbsimple.Movies(now['id']).keywords())
        context['populars'] = populars
        context['keywords'] = keywords
        context['pop_pages'] = range(1, populars['total_pages'])
        context['page_lead_in'] = page_lead_in
        context['page_lead_out'] = page_lead_out
        context['genre'] = genre.movie_list()
        context['nowplaying'] = nowplaying['results'][:8]

        context['request'] = self.request
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
