import json

import tmdbsimple
from django.conf import settings
from django.core.paginator import PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.views import generic

from search import models
from subworld.Paginator import Paginator
from subworld.views import BaseSetMixin


# Create your views here.

class MultiSearch(BaseSetMixin, generic.TemplateView):
    template_name = 'search/search_multi.html'
    locator = 'search'

    def get_context_data(self, **kwargs):
        context = super(MultiSearch, self).get_context_data(**kwargs)

        if self.request.GET:
            tmdbsimple.API_KEY = settings.TMDB_API_KEY

            page = int(self.request.GET.get('page', 1))
            if self.request.GET.get('search'):
                search = self.request.GET.get('search')
            else:
                search = ''
            print("searching: ", search)
            tmdbSearch = tmdbsimple.Search()

            list = tmdbSearch.multi(query=search, page=page)
            paginator = Paginator(object_lists=list['results'], total_results=list['total_results'],
                                  total_pages=list['total_pages'])

            try:
                paginator = paginator.get_page(page)
            except PageNotAnInteger:
                paginator = paginator.get_page(1)
            except EmptyPage:
                paginator = paginator.get_page(paginator.num_pages())

            context['page'] = page
            context['lists'] = list
            context['paginator'] = paginator

        return context


class MovieSearch(BaseSetMixin, generic.TemplateView):
    template_name = 'search/search_movie.html'


class ShowSearch(BaseSetMixin, generic.TemplateView):
    template_name = 'search/search_movie.html'


class EpisodeSearch(BaseSetMixin, generic.TemplateView):
    template_name = 'search/search_movie.html'


class CollectionSearch(BaseSetMixin, generic.TemplateView):
    template_name = 'search/search_movie.html'


class PersonSearch(BaseSetMixin, generic.TemplateView):
    template_name = 'search/search_movie.html'


def autocomplete(request):
    result = []
    if request.is_ajax():
        search = request.GET.get('term', default="")
        db = search_data(models.MovieDB, search)
        for r in db:
            result.append(r.original_title)
        tv = search_data(models.TvSeriesDB, search)
        for r in tv:
            result.append(r.original_name)

    data = json.dumps(result)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def tv_autocomplete(request):
    result = []
    if request.is_ajax():
        search = request.GET.get('term', default="")
        db = search_data(models.TvSeriesDB, search)
        for r in db:
            result.append(r.original_name)

    data = json.dumps(result)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def search_data(model, search):
    if model is models.MovieDB:
        return model.objects.filter(original_title__icontains=search)[:10]
    elif model is models.TvSeriesDB:
        return model.objects.filter(original_name__icontains=search)[:10]


def autoinfo(request):
    print('autoinfo')
    print(request.GET)
    if request.is_ajax():
        search = request.GET.get('term', default='')

    return None
