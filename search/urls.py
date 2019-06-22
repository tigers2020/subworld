from django.urls import path

from search import views

SEARCH_TYPE = [
]

urlpatterns = [
    path("movie_autocomplete/", views.movie_autocomplete, name='movie_autocomplete'),
    path("tv_autocomplete/", views.tv_autocomplete, name="tv_autocomplete"),
    path('autoinfo/<int:db_id>/', views.autoinfo, name="autoinfo"),
    path("", views.MultiSearch.as_view(), name='search'),
    path('movies/', views.MovieSearch.as_view(), name='search_movies'),
    path('shows/', views.TvShowSearch.as_view(), name='search_shows'),
    # path('collections/', views.CollectionSearch.as_view(), name='search_collections'),
    # path('people', views.PersonSearch.as_view(), name='search_people'),

    # path("movie/", views.MovieSearch.asview(), name="movie_search"),
    # path("movie/<int:movie_id>/detail/", views.MovieDetail.as_view(), name="movie_detail"),
    # path("tv/<int:id>/detail/", views.TvDetail.as_view(), name="tv_detail"),
    # path("people/<int:id>/detail/", views.PeopelDetail.as_view(), name="people_detail"),

]
