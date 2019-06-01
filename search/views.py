import json

from django.views import generic

from search import models
from django.forms.models import modelform_factory


# Create your views here.


class Search(generic.TemplateView):
    def get_context_data(self, **kwargs):
        context = super(Search, self).get_context_data(**kwargs)

        return context


def check_db(db, data):
    with open(data, encoding="UTF-8") as f:
        for line in f:
            json_data = json.loads(line)
            if db.filter(id=json_data['id']):
                print("data exist", json_data)
            else:
                print("create", json_data)
                db.create(**json_data)


class DbInit(generic.TemplateView):
    template_name = 'init.html'

    def get_context_data(self, **kwargs):
        context = super(DbInit, self).get_context_data(**kwargs)

        movie = models.MovieDB.objects.all()
        collection = models.CollectionDB.objects.all()
        tv_series = models.TvSeriesDB.objects.all()
        production_company = models.ProductionCompanyDB.objects.all()
        person = models.PersonDB.objects.all()
        keyword = models.KeywordDB.objects.all()
        tv_network = models.TvNetworkDB.objects.all()

        check_data = {}

        check_db(movie, "dataset/movie_ids_05_28_2019.json")
        check_db(collection, "dataset/collection_ids_05_28_2019.json")
        check_db(tv_series, "dataset/tv_series_ids_05_28_2019.json")
        check_db(production_company, "dataset/production_company_ids_05_28_2019.json")
        check_db(person, "dataset/person_ids_05_28_2019.json")
        check_db(keyword, "dataset/keyword_ids_05_28_2019.json")
        check_db(tv_network, "dataset/tv_network_ids_05_28_2019.json")

        if movie:
            check_data['movie'] = True
        else:
            check_data['movie'] = False

        if collection:
            check_data['collection'] = True
        else:
            check_data['collection'] = False
        if tv_series:
            check_data['tv_series'] = True
        else:
            check_data['tv_series'] = False
        if production_company:
            check_data['company'] = True
        else:
            check_data['company'] = False
        if person:
            check_data['person'] = True
        else:
            check_data['person'] = False
        if keyword:
            check_data['keyword'] = True
        else:
            check_data['keyword'] = False
        if tv_network:
            check_data['tv_network'] = True
        else:
            check_data['tv_network'] = False

        context['check_data'] = check_data
        context['movies'] = movie
        context['collections'] = collection
        context['tv_series'] = tv_series
        context['production_companies'] = production_company
        context['persons'] = person
        context['keywords'] = keyword
        context['tv_network'] = tv_network

        return context



