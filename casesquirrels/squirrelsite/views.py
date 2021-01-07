from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from django.contrib.auth import authenticate, login

from .models import Merch
from .forms import NewUserForm


class IndexView(generic.TemplateView):
    template_name = 'squirrelsite/index.html'

class SecretView(LoginRequiredMixin, generic.TemplateView):
    template_name=  'squirrelsite/secret.html'

# class NewUserView(generic.TemplateView):
#     template_name = 'squirrelsite/newuser.html'

def signup(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('squirrels:index')
    else:
        form = NewUserForm()
    return render(request, 'squirrelsite/newuser.html', {'form':form})