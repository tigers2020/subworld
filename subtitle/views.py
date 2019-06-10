# Create your views here.
import os

import tmdbsimple
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy
from django.views import generic

from subtitle.models import Subtitle
from .forms import SubtitleForm


class MovieDetailList(generic.ListView):
    model = Subtitle
    ordering = ('title', 'language',)

    def get_queryset(self):
        print("kwargs: ", self.kwargs)
        queryset = Subtitle.objects.filter(db_id=self.kwargs['db_id'])

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(MovieDetailList, self).get_context_data(*args, **kwargs)
        tmdbsimple.API_KEY = settings.TMDB_API_KEY
        movie = tmdbsimple.Movies(id=self.kwargs['db_id'])

        context['image_url'] = settings.BASE_DIR
        context['poster_size'] = settings.TMDB_POSTER_SIZE
        context['backdrop_size'] = settings.TMDB_BACKDROP_SIZE
        context['movie'] = movie.info()
        context['images'] = movie.images()
        context['persons'] = movie.credits()
        context['videos'] = movie.videos()
        context['similar'] = movie.similar_movies()
        context['keywords'] = movie.keywords()
        return context


class TvDetail(generic.ListView):
    model = Subtitle

    def get_queryset(self, **kwargs):
        query = super(TvDetail, self).get_queryset()

        return query


class CreateSubView(generic.CreateView):
    model = Subtitle
    form_class = SubtitleForm

    def get_success_url(self, **kwargs):

        return reverse_lazy("movie_detail", args=(self.object.db_id,))

    def form_invalid(self, form):
        print(form.errors)

        return super(CreateSubView, self).form_invalid(form)
    def form_valid(self, form):
        print(form.cleaned_data)
        subtitle = form.save(commit=False)
        subtitle.user = self.request.user
        if self.request.FILES:
            upload_file = self.request.FILES['sub_file']
            subtitles = Subtitle.objects.all()
            if upload_file.name in subtitles:
                print("file is already exist.")
            path_1 = ""
            fs = FileSystemStorage()

            video_type = subtitle.type
            db_id = subtitle.db_id
            language = subtitle.language

            if video_type == 1:
                path_1 = "movie"
            elif video_type == 2:
                path_1 = "tv"
            file_path = os.path.join(path_1, str(db_id), language.iso_639_1, upload_file.name)
            print(file_path)
            fs.save(file_path, upload_file)

            form.user = self.request.user
            form.save()
            return super(CreateSubView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateSubView, self).get_context_data(**kwargs)

        if self.request.GET:
            tmdbsimple.API_KEY = settings.TMDB_API_KEY
            if self.request.GET.get('movie_id'):
                context['info'] = tmdbsimple.Movies(self.request.GET.get('movie_id')).info()
                context['show_type'] = 1
            elif self.request.GET.get('tv_show_id'):
                context['info'] = tmdbsimple.TV(self.request.GET.get('tv_show_id')).info()
                context['show_type'] = 2

            context['image_url'] = settings.TMDB_IMAGE_BASE
            context['poster_size'] = settings.TMDB_POSTER_SIZE
            return context

        return context
