from django.urls import path
from search import views

SEARCH_TYPE = [
]

urlpatterns = [
    path("autocomplete/", views.autocomplete, name='autocomplete'),
    path('autoinfo/', views.autoinfo, name="autoinfo"),
    path("", views.Search.as_view(), name='search'),
    # path("movie/", views.MovieSearch.asview(), name="movie_search"),
    # path("movie/<int:movie_id>/detail/", views.MovieDetail.as_view(), name="movie_detail"),
    # path("tv/<int:id>/detail/", views.TvDetail.as_view(), name="tv_detail"),
    # path("people/<int:id>/detail/", views.PeopelDetail.as_view(), name="people_detail"),


]
