import json

from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.db.models import Q
from django.utils.safestring import mark_safe

from .forms import RegistrationForm, SingInForm, AddNewForm, MatchForm, ScoringForm
from .models import Players, Matches, TablesView, News, Scoring, MatchEvent, TransMatch
from django.views.generic import CreateView, UpdateView

from shop.models import Products


def fail_404(request, exception):
    return render(request, '404.html', status=404)


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
    if not request.user.is_superuser:
        return redirect('home')
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

    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('home')
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)


def del_new(request, id_news):
    if not request.user.is_superuser:
        return redirect('home')
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
    return render(request, 'main/Matches.html', {'matches': matchs})


def add_match(request):
    if not request.user.is_superuser:
        return redirect('home')
    if request.method == 'POST':
        form = MatchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('all_matches')
    else:
        form = MatchForm()
    return render(request, 'main/Add_Match.html', {'form': form})


def match(request, slug_match):
    mtch = Matches.objects.get(slug=slug_match)
    if mtch.pk == int(Matches.objects.order_by('-date')[0].pk):
        return redirect('live_match', slug_match)
    scr = Scoring.objects.filter(match_id=mtch.id)
    if TransMatch.objects.filter(match_id=mtch.id):
        trans = TransMatch.objects.get(match_id=mtch.id)
        mtch_vt = MatchEvent.objects.filter(trans_id=trans.id).order_by('-timestamp')
        return render(request, 'main/StatsMatch.html', {
            'mtch': mtch,
            'scr': scr,
            'mtch_vt': mtch_vt,
            'trans': trans
        })
    return render(request, 'main/StatsMatch.html', {
        'mtch': mtch,
        'scr': scr
    })


def all_matches(request):
    matchs = Matches.objects.all().order_by('-date')
    return render(request, 'main/All_Matches.html', {'matches': matchs})


class MatchUpdateView(UpdateView):
    model = Matches
    template_name = 'main/Upd_Match.html'
    form_class = MatchForm

    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('home')
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)


def editor_scoring(request, slug_match):
    match = Matches.objects.get(slug=slug_match)
    scr = Scoring.objects.filter(match_id=match.pk)
    if request.method == "POST":
        f = ScoringForm(request.POST)
        print(request.POST.getlist('score'))
        if f.is_valid():
            plr = Players.objects.get(pk=request.POST['player'])
            if not Scoring.objects.filter(match_id=match.pk, player_id=plr.pk):
                Scoring.objects.create(player=plr, match=match)
        if request.POST.getlist('score'):
            for s in scr:
                name = 'goals-' + str(s.pk)
                s.score = request.POST[name]
                s.save()

    form = ScoringForm()

    return render(request, 'main/Editor_Scoring.html', {'form': form, 'match': match, 'scr': scr})


def del_scoring(request, slug_match, id_scoring):
    if not request.user.is_superuser:
        return redirect('home')
    scr = Scoring.objects.get(pk=id_scoring)
    scr.delete()
    return redirect('editor_scoring', slug_match)


def del_match(request, id_match):
    if not request.user.is_superuser:
        return redirect('home')
    m = Matches.objects.get(pk=id_match)
    m.delete()
    return redirect('match')


def live_match(request, slug_match):
    mtch = Matches.objects.get(slug=slug_match)
    if not TransMatch.objects.filter(match_id=mtch.id):
        TransMatch.objects.create(match=mtch)
    user = mark_safe(json.dumps(''))
    if request.user.is_authenticated:
        user = mark_safe(json.dumps(request.user.email))
    scr = Scoring.objects.filter(match_id=mtch.id)
    trans = TransMatch.objects.get(match_id=mtch.id)
    timer = 'false'
    if (trans.start_1 and not trans.pause) or (trans.start_2 and not trans.end):
        timer = 'true'
    return render(request, 'main/Live_match.html', {
        'mtch': mtch,
        'scr': scr,
        'username': user,
        'trans': trans,
        'timer': timer
    })


def table(request):
    table_str = TablesView.objects.all()
    return render(request, 'main/Table.html', {'table_str': table_str})


def achievements(request):
    return render(request, 'main/Achievements.html')
