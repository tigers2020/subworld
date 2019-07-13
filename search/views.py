import json

import tmdbsimple
from django.conf import settings
from django.core.paginator import PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.views import generic

from search import models
from subtitle.models import TvSeriesDB, MovieDB
from subworld.Paginator import Paginator
from subworld.views import BaseSetMixin, create_update_db


# Create your views here.

def searching(context, object_lists, page):
    print(object_lists)
    paginator = Paginator(object_lists=object_lists['total_results'], total_results=object_lists['total_results'],
                          total_pages=object_lists['total_pages'])
    try:
        paginator = paginator.get_page(page)
    except PageNotAnInteger:
        paginator = paginator.get_page(1)
    except EmptyPage:
        paginator = paginator.get_page(paginator.num_pages)

    context['page'] = page
    context['lists'] = object_lists
    context['paginator'] = paginator

    return context


class MultiSearch(BaseSetMixin, generic.TemplateView):
    template_name = 'search/search_multi.html'
    locator = 'search'

    def get_context_data(self, **kwargs):
        context = super(MultiSearch, self).get_context_data(**kwargs)
        if self.request.GET:
            tmdbsimple.API_KEY = settings.TMDB_API_KEY
            page = int(self.request.GET.get('page', 1))
            query = self.request.GET.get('search', "")
            tmdb_search = tmdbsimple.Search()
            context = searching(context, tmdb_search.multi(query=query, page=page), page)
        return context


class MovieSearch(BaseSetMixin, generic.TemplateView):
    template_name = 'search/search_movie.html'
    locator = 'search_movie'

    def get_context_data(self, **kwargs):
        context = super(MovieSearch, self).get_context_data(**kwargs)
        if self.request.GET:
            tmdbsimple.API_KEY = settings.TMDB_API_KEY
            page = int(self.request.GET.get('page', 1))
            query = self.request.GET.get('search', "")
            tmdb_search = tmdbsimple.Search()
            context = searching(context, tmdb_search.movie(query=query, page=page), page)
        return context


class TvShowSearch(BaseSetMixin, generic.TemplateView):
    template_name = 'search/search_tv_show.html'
    locator = 'search_tv_show'

    def get_context_data(self, **kwargs):
        context = super(TvShowSearch, self).get_context_data(**kwargs)
        if self.request.GET:
            tmdbsimple.API_KEY = settings.TMDB_API_KEY
            page = int(self.request.GET.get('page', 1))
            query = self.request.GET.get('search', "")
            tmdb_search = tmdbsimple.Search()
            context = searching(context, tmdb_search.tv(query=query, page=page), page)
        return context

def autocomplete(request):
    result = []
    if request.is_ajax():
        print(request)
        if request.GET['type'] == 'tv_show':
            search = request.GET.get('search', default="")
            db = search_data(models.TvSeriesDB, search)
            for r in db:
                if r.name == "" or r.name is None:
                    print("name", r)
                    result.append({
                        'label': r.original_name,
                        'value': r.id,
                    })
                else:
                    result.append({
                        'label': r.original_name,
                        'value': r.id,
                    })
        elif request.GET['type'] == "movie":
            search = request.GET.get('search', default="")
            db = search_data(models.MovieDB, search)
            for r in db:
                if r.title == "" or r.title is None:
                    print("name", r)
                    result.append({
                        'label': r.original_title,
                        'value': r.id,
                    })
                else:
                    result.append({
                        'label': r.title,
                        'value': r.id,
                    })
        data = json.dumps(result)
        mimetype = 'application/json'
        return HttpResponse(data, mimetype)


def search_data(model, search):
    if model is models.MovieDB:
        return model.objects.filter(Q(original_title__icontains=search) | Q(title__icontains=search))[:10]
    elif model is models.TvSeriesDB:
        return model.objects.filter(Q(original_name__icontains=search) | Q(name__icontains=search))[:10]


def auto_info(request):
    detail = []
    if request.is_ajax():
        tmdb = tmdbsimple
        tmdb.API_KEY = settings.TMDB_API_KEY
        db_id = request.GET.get('db_id', 1)
        if request.GET['type'] == "tv_show":
            detail = tmdb.TV(id=db_id).info()
            create_update_db(TvSeriesDB, detail)
        if request.GET['type'] == "movie":
            detail = tmdb.Movies(id=db_id).info()
            create_update_db(MovieDB, detail)

        return JsonResponse(detail)
