import uuid

from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.
from django.template.loader import render_to_string
from django.views.generic import TemplateView

from moviedb import models
from subworld.views import BaseSetMixin


def get_db_from_model(argument):
    switcher = {
        1: models.Genre,
        2: models.Country,
        3: models.Language,
        4: models.Movie,
        5: models.Person,
        6: models.Keyword,
        7: models.Network,
        8: models.Tv,
        9: models.Collection
    }

    return switcher.get(argument, "no db found")


def check_db(request):
    context = {}
    if request.POST:
        db_type = int(request.POST.get('db_type'))
        db = get_db_from_model(db_type)
        print("get db: ", db)

        context['db_type'] = db_type
        context['name'] = db.__name__
        context['database'] = db.objects.all()

    return render(request, 'movie_db/check_db.html', context)


def init_db(request):
    context = {}
    if request.POST:
        db_type = int(request.POST.get('db_type'))
        db = get_db_from_model(db_type)

        print("initiating db: ", db)

        inited_db = db().initiate_data()

        if inited_db.exists() or inited_db.exists() is not None:
            context['database'] = inited_db.all()
            context['success'] = "Initiating complete"
        else:
            context['failed'] = "Initiating Failed"

    return render(request, 'movie_db/init_db.html', context)


class CheckDBLIst(TemplateView, BaseSetMixin):
    template_name = 'movie_db/index.html'

    def get_context_data(self, **kwargs):
        context = super(CheckDBLIst, self).get_context_data(**kwargs)

        database = []
        for i in range(1, 10):
            db = get_db_from_model(i)

            database.append({'name': db.__name__, 'queryset': db.objects.all()})

        context['database'] = database

        return context


class Monitor(TemplateView):
    template_name = 'movie_db/monitor.html'


def ajax_monitor(request):
    if request.is_ajax():
        if request.GET:
            print(request)
            db_type = request.GET.get('db_type')
            name = uuid.uuid4().hex[:6].upper()
            html = render_to_string('movie_db/monitor_list.html', {'db_type': db_type, 'name': name})
            return HttpResponse(html)
    return "Failed"
