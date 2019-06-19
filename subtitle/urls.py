"""subworld URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
    """
from django.urls import path

from subtitle import views

urlpatterns = [
    path("movie/<int:db_id>", views.MovieDetailList.as_view(), name="movie_detail"),
    path("tv/<int:db_id>", views.TvDetailList.as_view(), name="tv_detail"),
    path("tv/<int:db_id>/season/<int:season_number>/", views.TvSeasonList.as_view(), name="tv_seasons"),
    path("tv/<int:db_id>/season/<int:season_number>/episode/<int:episode_number>", views.TvEpisodeList.as_view(), name="tv_seasons"),
    # path("collection/<int:id>", views.CollectionDetail.as_view(), name="collection_detail"),
    path("upload", views.CreateMovieSubView.as_view(), name="sub-upload"),
]
