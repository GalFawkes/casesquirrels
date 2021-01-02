from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import generic

from .models import Merch


class IndexView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'squirrelsite/index.html'

class SecretView(LoginRequiredMixin, generic.TemplateView):
    template_name=  'squirrelsite/secret.html'
