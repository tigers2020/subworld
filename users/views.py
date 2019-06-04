from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views import generic
from .forms import  SubUserCreationForm


class SignUp(generic.CreateView):
    form_class = SubUserCreationForm
    success_url = reverse_lazy('login')
    template_name = "registration/signup.html"



class Test(generic.TemplateView):
    template_name = "forum/test.html"