from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.db.models import Q

from .forms import RegistrationForm, SingInForm, AddNewForm
from .models import Players, Matches, TablesView, News
from django.views.generic import CreateView, UpdateView


def home(request):
    news = News.objects.order_by('-date_time')[:3]
    return render(request, 'main/Home.html', {'news': news})


def all_news(request):
    news = News.objects.order_by('-date_time')
    return render(request, 'main/News.html', {'news': news})


def news(request, news_slug):
    n = News.objects.get(slug=news_slug)
    three_news = News.objects.order_by('-date_time')[:3]
    return render(request, 'main/OneNews.html', {'news': n, 'three_news': three_news})


def add_new(request):
    if request.method == 'POST':
        form = AddNewForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('all_news')
    else:
        form = AddNewForm()

    return render(request, 'main/Add_New.html', {'form': form})


class NewsUpdateView(UpdateView):
    model = News
    template_name = 'main/Upd_News.html'
    form_class = AddNewForm


def del_new(request, id_news):
    n = News.objects.get(pk=id_news)
    n.delete()
    return redirect('all_news')


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


def details_player(request, slug_player):
    plr = Players.objects.get(slug=slug_player)
    return render(request, 'main/Details_player.html', {'plr': plr})


def matches(request):
    matchs = Matches.objects.filter(Q(home_team__q_we=True) | Q(away_team__q_we=True)).order_by('-date')
    return render(request, 'main/Match.html', {'matches': matchs})


def table(request):
    table_str = TablesView.objects.all()

    return render(request, 'main/Table.html', {'table_str': table_str})


def achievements(request):
    return render(request, 'main/Achievements.html')
