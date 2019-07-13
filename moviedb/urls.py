from django.urls import path

from moviedb import views

SEARCH_TYPE = [
]

urlpatterns = [
    path("check_db/", views.check_db, name="check-db"),
    path('', views.CheckDBLIst.as_view(), name='moviedb_index'),
    path('init_db/', views.init_db, name='init-db'),
]
