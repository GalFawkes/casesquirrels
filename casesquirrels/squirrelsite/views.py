from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from django.contrib.auth import authenticate, login

from .models import Merch, Score
from .forms import NewUserForm, SolutionForm


class IndexView(generic.TemplateView):  # Need to implement each item of merchandise being displayed
    template_name = 'squirrelsite/index.html'

class SecretView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'squirrelsite/secret.html'

class RedeemView(LoginRequiredMixin, generic.edit.FormView):
    template_name='squirrelsite/redeem.html'
    form_class = SolutionForm
    success_url = '/site'

    def form_valid(self, form):
        form.validate(self.request.user)
        return super().form_valid(form)

class LeaderboardView(LoginRequiredMixin, generic.list.ListView):
    model = Score


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