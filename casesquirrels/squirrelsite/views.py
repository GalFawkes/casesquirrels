from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from django.contrib.auth import authenticate, login


from .models import Merch, Score, Squad, SquadMember
from .forms import NewUserForm, SolutionForm


class IndexView(generic.ListView):  # Need to implement each item of merchandise being displayed
    template_name = 'squirrelsite/index.html'

    def get_queryset(self):
        results = Merch.objects.all()
        return results

class SecretView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'squirrelsite/secret.html'

class RedeemView(LoginRequiredMixin, generic.edit.FormView):
    template_name='squirrelsite/redeem.html'
    form_class = SolutionForm
    success_url = '/site/leaderboard'

    def form_valid(self, form):
        # THIS IS SHITTY DESIGN AND SHOULD BE BURNED
        result = form.validate(self.request.user)
        if result:
            return super().form_valid(form)
        else:
            return super().form_invalid(form)

class LeaderboardView(LoginRequiredMixin, generic.list.ListView):
    template_name='squirrelsite/leaderboard.html'
    
    def get_queryset(self):
        # Get all squads updated (gives scores)
        # Filter all users in squads out
        # ???
        # profit
        for squad in Squad.objects.all():
            squad.make_user()  # I hate my life right now
        results = Score.objects.order_by('-points')
        squad_members = SquadMember.objects.all()
        member_list = []
        for member in squad_members:
            member_list.append(member.player)
        results = results.exclude(user__in=member_list)
        return results


def signup(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            new_score = Score(user=user)
            new_score.save()
            login(request, user)
            return redirect('squirrels:index')
    else:
        form = NewUserForm()
    return render(request, 'squirrelsite/newuser.html', {'form':form})