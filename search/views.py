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
            tmdbSearch = tmdbsimple.Search()

            movie_list = tmdbSearch.movie(query=search)

            context['image_url'] = settings.TMDB_IMAGE_BASE
            context['image_size'] = settings.TMDB_POSTER_SIZE
            context['movie_lists'] = movie_list

        return context


def autocomplete(request):
    result = []
    print("autocomplete")
    if request.is_ajax():
        print("is ajax")
        print("request", request.GET)
        search = request.GET.get('term', default="")
        print('search', search)
        db = models.MovieDB.objects.filter(original_title__icontains=search)[:10]
    else:
        db = models.MovieDB.objects.order_by("-popularity")[:10]
    for r in db:
        result.append(r.original_title)

    data = json.dumps(result)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
