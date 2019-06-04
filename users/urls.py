from django.urls import path
from . import views

urlpatterns = [
    path("test", views.Test.as_view(), name = "test"),
    path('signup/', views.SignUp.as_view(), name = "signup"),
]