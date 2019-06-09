# Create your views here.
import os

import tmdbsimple
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy
from django.views import generic

from subtitle.models import Subtitle
from .forms import SubtitleForm


class MovieDetail(generic.ListView):
    model = Subtitle

    def get_context_data(self, *args, **kwargs):
        context = super(MovieDetail, self).get_context_data(*args, **kwargs)
        tmdbsimple.API_KEY = settings.TMDB_API_KEY
        movie = tmdbsimple.Movies(id=self.kwargs['id'])

        context['movie'] = movie.info()
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

    def form_valid(self, form):
        print(form.cleaned_data)
        if self.request.FILES:
            upload_file = self.request.FILES['sub_file']
            path_1 = ""
            fs = FileSystemStorage()

            video_type = form.cleaned_data['type']
            db_id = form.cleaned_data['db_id']

            if video_type == 1:
                path_1 = "movie"
            elif video_type == 2:
                path_1 = "tv"
            file_path = os.path.join(path_1, str(db_id), upload_file.name)
            print(file_path)
            fs.save(file_path, upload_file)

            form.user = self.request.user
            return super(CreateSubView, self).form_valid(form)

    def form_invalid(self, form):
        print("form error: ", form.errors)

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
