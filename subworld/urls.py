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
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.IndexView.as_view(), name='index'),
    path('movie/', views.MovieIndexView.as_view(), name='movie_index'),
    path('tv_show/', views.TvShowIndexView.as_view(), name='tv_show_index'),
    path('d/', include('subtitle.urls')),
    path('s/', include('search.urls')),
    # path("checkdb", views.DbInit.as_view(), name='db_init'),
    path("users/", include("users.urls")),
    path("accounts/", include("allauth.urls")),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('moviedb/', include('moviedb.urls')),
]

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
