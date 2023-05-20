import json

from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.db.models import Q
from django.utils.safestring import mark_safe

from .forms import RegistrationForm, SingInForm, AddNewForm
from .models import Players, Matches, TablesView, News, Scoring, MatchEvent
from django.views.generic import CreateView, UpdateView

from shop.models import Products


def home(request):
    news = News.objects.order_by('-date_time')[:3]
    players = Players.objects.order_by('number')
    merch1 = Products.objects.filter(Q(cat_id=1) & Q(kind_id=1)).order_by('-year')[:1]
    merch2 = Products.objects.filter(Q(cat_id=2) & Q(kind_id=1)).order_by('-year')[:1]
    merch3 = Products.objects.filter(Q(cat_id=3) & Q(kind_id=1)).order_by('-year')[:1]
    return render(request, 'main/Home.html',
                  {'news': news, 'plrs': players,
                   'm1': merch1, 'm2': merch2, 'm3': merch3})


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


def match(request, slug_match):
    mtch = Matches.objects.get(slug=slug_match)
    scr = Scoring.objects.filter(match_id=mtch.id)
    mtch_vt = MatchEvent.objects.filter(match_id=mtch.id)
    return render(request, 'main/StatsMatch.html', {
        'mtch': mtch,
        'scr': scr,
        'mtch_vt': mtch_vt,
    })


def live_match(request, slug_match):
    mtch = Matches.objects.get(slug=slug_match)
    scr = Scoring.objects.filter(match_id=mtch.id)
    return render(request, 'main/Live_match.html', {
        'mtch': mtch,
        'scr': scr,
        'username': mark_safe(json.dumps(request.user.email))
    })


def table(request):
    table_str = TablesView.objects.all()
    return render(request, 'main/Table.html', {'table_str': table_str})


def achievements(request):
    return render(request, 'main/Achievements.html')
