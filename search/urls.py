from django.urls import path

from search import views

SEARCH_TYPE = [
]

urlpatterns = [
    path("tv_autocomplete/", views.autocomplete, name="tv_autocomplete"),
    path('auto_info/', views.auto_info, name="auto-info"),
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
