from django.shortcuts import render
from django.views import generic
# Create your views here.


class Search(generic.TemplateView):
    def get_context_data(self, **kwargs):
        context = super(Search, self).get_context_data(**kwargs)

        return context
