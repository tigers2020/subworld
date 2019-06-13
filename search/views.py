import json

import tmdbsimple
from django.conf import settings
from django.http import HttpResponse
from django.views import generic

from search import models


# Create your views here.


class Search(generic.TemplateView):
    template_name = 'search/search_movie.html'

    def get_context_data(self, **kwargs):
        context = super(Search, self).get_context_data(**kwargs)

        if self.request.GET:
            tmdbsimple.API_KEY = settings.TMDB_API_KEY

            search = self.request.GET.get('search')
            print("searching: ", search)
            tmdbSearch = tmdbsimple.Search()

            movie_list = tmdbSearch.movie(query=search)

            print(movie_list)
            context['image_url'] = settings.TMDB_IMAGE_BASE
            context['image_size'] = settings.TMDB_POSTER_SIZE
            context['movie_lists'] = movie_list

        return context


def autocomplete(request):
    result = []
    if request.is_ajax():
        search = request.GET.get('term', default="")
        db = search_data(models.MovieDB, search)
        for r in db:
            result.append(r.original_title)

    data = json.dumps(result)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def tv_autocomplete(request):
    result = []
    if request.is_ajax():
        search = request.GET.get('term', default="")
        db = search_data(models.TvSeriesDB, search)
        for r in db:
            result.append(r.original_title)

    data = json.dumps(result)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def search_data(model, search):
    if model == models.MovieDB:
        return model.objects.filter(original_title__icontains=search)[:10]
    elif model == models.TvSeriesDB:
        return model.objects.filter(original_name__icontains=search)[:10]


def autoinfo(request):
    print('autoinfo')
    print(request.GET)
    if request.is_ajax():
        search = request.GET.get('term', default='')

    return None
