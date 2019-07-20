# Create your views here.
import os

import tmdbsimple
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy
from django.views import generic

from moviedb.models import Movie, TvSeries, Credit, Videos, Keyword
from subtitle.models import MovieSubtitleInfo, TvSubtitleInfo
from subworld.views import BaseSetMixin, create_update_db
from .forms import MovieSubtitleForm, TvShowSubtitleForm


class MovieDetailWithSubtitleList(BaseSetMixin, generic.ListView):
    model = MovieSubtitleInfo
    ordering = ('title', 'language',)
    locator = "movie_detail"
    template_name = 'subtitle/movie_detail.html'

    def get_queryset(self):
        print("kwargs: ", self.kwargs)
        queryset = MovieSubtitleInfo.objects.filter(movie_id=self.kwargs['db_id'])[:20]

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(MovieDetailWithSubtitleList, self).get_context_data(*args, **kwargs)
        movie_id = self.kwargs['db_id']
        movie = Movie.initialize.get_or_create_movie(movie_id=movie_id)
        credit = Credit.movie_initialize.update_or_create_credit(movie_id=movie_id)
        video = Videos.movie_initialize.get_or_create_video(movie_id=movie_id)
        keyword = Movie.initialize.get_or_create_movie(movie_id).keyword

        context['movie'] = movie
        context['credits'] = credit
        context['videos'] = video
        context['keywords'] = keyword
        return context


class TvDetailList(BaseSetMixin, generic.ListView):
    model = TvSubtitleInfo
    template_name = 'subtitle/tv_show_subtitle_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(TvDetailList, self).get_context_data(*args, **kwargs)
        tv_show = self.tmdb.TV(id=self.kwargs['db_id'])
        create_update_db(TvSeries, tv_show.info())
        context['tv_show'] = tv_show.info()
        context['images'] = tv_show.images()
        context['videos'] = tv_show.videos()
        context['persons'] = tv_show.credits()

        return context


class TvSeasonList(BaseSetMixin, generic.ListView):
    model = TvSubtitleInfo
    template_name = 'subtitle/tv_season_subtitle_list.html'


class TvEpisodeList(BaseSetMixin, generic.ListView):
    model = TvSubtitleInfo
    template_name = 'subtitle/tv_episode_subtitle_list.html'


class CreateMovieSubView(BaseSetMixin, generic.CreateView):
    model = MovieSubtitleInfo
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
            subtitles = MovieSubtitleInfo.objects.all()
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
            context['info'] = tmdbsimple.Movies(self.request.GET.get('movie_id')).info()
            return context

        return context


class CollectionDetail(generic.TemplateView):
    pass


class CreateTvSubView(BaseSetMixin, generic.CreateView):
    model = TvSubtitleInfo
    form_class = TvShowSubtitleForm
    locator = 'upload_tv_show'

    def get_success_url(self, **kwargs):
        return reverse_lazy("tv_detail", args=(self.object.db_id.pk,))

    def get_context_data(self, **kwargs):
        context = super(CreateTvSubView, self).get_context_data(**kwargs)
        if self.request.GET:
            tmdbsimple.API_KEY = settings.TMDB_API_KEY
            context['info'] = tmdbsimple.TV(self.request.GET.get('tv_id')).info()
            return context

        return context
