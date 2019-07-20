from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.
from django.template.loader import render_to_string
from django.views.generic import TemplateView

from moviedb import models
from subworld.views import BaseSetMixin

SWITCHER = {
    'genre': models.Genre,
    'country': models.Country,
    'company': models.Company,
    'language': models.Language,
    'movie': models.Movie,
    'person': models.Person,
    'keyword': models.Keyword,
    'network': models.Network,
    'tv': models.TvSeries,
    'tv_season': models.TvSeason,
    'tv_episode': models.TvEpisode,
    'collection': models.Collection
}
NO_DATA_ID = 9999999


def get_db_from_model(argument):
    return SWITCHER.get(argument, "no db found")


def check_db(request):
    context = {}
    if request.POST:
        db_type = request.POST.get('db_type')
        db = get_db_from_model(db_type)
        print("get db: ", db, db_type)

        context['db_type'] = db_type
        context['name'] = db.__name__

    return render(request, 'movie_db/check_db.html', context)


def initialize_no_data(request):
    OBJECTS = [
        models.Language,
        models.Country,
        models.Genre,
        models.Company,
        models.Keyword,
        models.Movie,
        models.Person,
        models.Network,
        models.TvEpisode,
        models.TvSeason,
        models.TvSeries,
        models.Collection,
    ]

    for objects in OBJECTS:

        obj, created = objects.initialize.update_or_create(id=NO_DATA_ID)

        if created:
            obj.save()
            print('{} no data been setup'.format(obj.__class__))
        else:
            print('{} no data already setup'.format(obj.__class__))

    return HttpResponse("OK")


def init_db(request):
    context = {}
    if request.POST:
        db_type = request.POST.get('db_type')
        db = get_db_from_model(db_type)

        print("initiating db: ", db)

        inited_db = db.initialize.initialize_data()

        if inited_db:
            context['count'] = db.initialize.count()
            context['success'] = "Initiating complete"
        else:
            context['failed'] = "Initiating Failed"

    return render(request, 'movie_db/init_db.html', context)


class CheckDBLIst(TemplateView, BaseSetMixin):
    template_name = 'movie_db/index.html'

    def get_context_data(self, **kwargs):
        context = super(CheckDBLIst, self).get_context_data(**kwargs)

        database = []
        for v in SWITCHER:
            db = get_db_from_model(v)
            database.append({
                'name': db.__name__, 'queryset': db.initialize.all().order_by('-id')[:20],
                'count': db.initialize.count()
            })

        context['database'] = database

        return context


class Monitor(TemplateView):
    template_name = 'movie_db/monitor.html'


def ajax_monitor(request):
    if request.is_ajax():
        if request.GET:
            db_type = request.GET.get('db_type')
            html = render_to_string('movie_db/monitor_list.html',
                                    {'db_type': db_type,
                                     'data': get_db_from_model(db_type).initialize.order_by('-id').all()[:5].values(),
                                     'count': get_db_from_model(db_type).initialize.count(),
                                     'tmdb': BaseSetMixin()
                                     })
            return HttpResponse(html)
    return "Failed"
