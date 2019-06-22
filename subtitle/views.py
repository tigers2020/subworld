# Create your views here.
import os

import tmdbsimple
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy
from django.views import generic

from search.models import MovieDB, TvSeriesDB
from subtitle.models import MovieSubtitle, TvSubtitle
from subworld.views import BaseSetMixin, create_update_db
from .forms import MovieSubtitleForm


class MovieDetailList(BaseSetMixin, generic.ListView):
    model = MovieSubtitle
    ordering = ('title', 'language',)
    locator = "movie_detail"
    template_name = 'subtitle/moviesubtitle_list.html'

    def get_queryset(self):
        print("kwargs: ", self.kwargs)
        queryset = MovieSubtitle.objects.filter(db_id_id=self.kwargs['db_id'])[:20]

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(MovieDetailList, self).get_context_data(*args, **kwargs)
        movie = tmdbsimple.Movies(id=self.kwargs['db_id'])

        create_update_db(MovieDB, movie.info())
        context['movie'] = movie.info()
        context['images'] = movie.images()
        context['persons'] = movie.credits()
        context['videos'] = movie.videos()
        context['keywords'] = movie.keywords()
        return context


class TvDetailList(BaseSetMixin, generic.ListView):
    model = TvSubtitle
    template_name = 'subtitle/tv_show_subtitle_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(TvDetailList, self).get_context_data(*args, **kwargs)
        tv_show = self.tmdb.TV(id=self.kwargs['db_id'])
        create_update_db(TvSeriesDB, tv_show.info())
        context['tv_show'] = tv_show.info()
        context['images'] = tv_show.images()
        context['videos'] = tv_show.videos()
        context['persons'] = tv_show.credits()

        return context


class TvSeasonList(BaseSetMixin, generic.ListView):
    model = TvSubtitle
    template_name = 'subtitle/tv_season_subtitle_list.html'


class TvEpisodeList(BaseSetMixin, generic.ListView):
    model = TvSubtitle
    template_name = 'subtitle/tv_episode_subtitle_list.html'


class CreateMovieSubView(BaseSetMixin, generic.CreateView):
    model = MovieSubtitle
    form_class = MovieSubtitleForm
    locator = 'upload_movie'

    def get_success_url(self, **kwargs):

        return reverse_lazy("movie_detail", args=(self.object.db_id.pk,))

    def form_invalid(self, form):
        print(form.errors)

        return super(CreateMovieSubView, self).form_invalid(form)

    def form_valid(self, form):
        print(form.cleaned_data)
        subtitle = form.save(commit=False)
        subtitle.user = self.request.user
        if self.request.FILES:
            upload_file = self.request.FILES['sub_file']
            subtitles = MovieSubtitle.objects.all()
            if upload_file.name in subtitles:
                print("file is already exist.")
            path_1 = ""
            fs = FileSystemStorage()

            db_id = subtitle.db_id
            language = subtitle.language

            file_path = os.path.join(path_1, str(db_id), language.iso_639_1, upload_file.name)
            print(file_path)
            fs.save(file_path, upload_file)

            form.user = self.request.user
            form.save()
            return super(CreateMovieSubView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateMovieSubView, self).get_context_data(**kwargs)

        if self.request.GET:
            tmdbsimple.API_KEY = settings.TMDB_API_KEY
            if self.request.GET.get('movie_id'):
                context['info'] = tmdbsimple.Movies(self.request.GET.get('movie_id')).info()
                context['show_type'] = 1
            elif self.request.GET.get('tv_show_id'):
                context['info'] = tmdbsimple.TV(self.request.GET.get('tv_show_id')).info()
                context['show_type'] = 2

            return context

        return context


class CollectionDetail(generic.TemplateView):
    pass
