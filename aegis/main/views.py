from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.db.models import Q

from .forms import RegistrationForm, SingInForm
from .models import Players, Matches, TablesView, Tables
from django.views.generic import CreateView


def home(request):
    return render(request, 'main/Home.html')


def history(request):
    return render(request, 'main/History.html')


class Registration(CreateView):
    form_class = RegistrationForm
    template_name = 'main/Registration.html'
    success_url = reverse_lazy('singIn')


class SingIn(LoginView):
    form_class = SingInForm
    template_name = 'main/SingIn.html'

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('home')


def players(request):
    players = Players.objects.order_by('number')
    return render(request, 'main/Players.html', {'players': players})


def matches(request):
    matchs = Matches.objects.filter(Q(home_team__q_we=True) | Q(away_team__q_we=True)).order_by('-date')

    return render(request, 'main/Match.html', {'matches': matchs})


def table(request):
    table_str = TablesView.objects.all()

    return render(request, 'main/Table.html', {'table_str': table_str})
