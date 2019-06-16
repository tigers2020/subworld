from django.urls import path

from search import views

SEARCH_TYPE = [
]

urlpatterns = [
    path("_autocomplete/", views.autocomplete, name="_autocomplete"),
    path("movie_autocomplete/", views.autocomplete, name='movie_autocomplete'),
    path("tv_autocomplete/", views.tv_autocomplete, name="tv_autocomplete"),
    path('autoinfo/', views.autoinfo, name="autoinfo"),
    path("", views.MultiSearch.as_view(), name='search'),
    path('movies/', views.MovieSearch.as_view(), name='search_movies'),
    path('shows/', views.ShowSearch.as_view(), name='search_shows'),
    path('episodes/', views.EpisodeSearch.as_view(), name='search_episodes'),
    path('collections/', views.CollectionSearch.as_view(), name='search_collections'),
    path('people', views.PersonSearch.as_view(), name='search_people'),

    # path("movie/", views.MovieSearch.asview(), name="movie_search"),
    # path("movie/<int:movie_id>/detail/", views.MovieDetail.as_view(), name="movie_detail"),
    # path("tv/<int:id>/detail/", views.TvDetail.as_view(), name="tv_detail"),
    # path("people/<int:id>/detail/", views.PeopelDetail.as_view(), name="people_detail"),

]
