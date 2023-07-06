import json

from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.db.models import Q
from django.utils.safestring import mark_safe

from .forms import RegistrationForm, SingInForm, AddNewForm, MatchForm, ScoringForm, PlayerForm, WebPasswordResetForm, \
    WebSetPasswordForm
from .models import *
from django.views.generic import CreateView, UpdateView

from shop.models import Products


def fail_404(request, exception):
    return render(request, '404.html', status=404)


def home(request):
    news = News.objects.order_by('-date_time')[:3]
    plrs = Players.objects.filter(out=None).order_by('number')
    merch1 = Products.objects.filter(Q(cat_id=1) & Q(kind_id=1)).order_by('-year')[:1]
    merch2 = Products.objects.filter(Q(cat_id=2) & Q(kind_id=1)).order_by('-year')[:1]
    merch3 = Products.objects.filter(Q(cat_id=3) & Q(kind_id=1)).order_by('-year')[:1]
    return render(request, 'main/Home.html',
                  {'news': news, 'plrs': plrs,
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


class WebPasswordReset(PasswordResetView):
    template_name = 'main/password_reset_email.html'
    form_class = WebPasswordResetForm


class WebPasswordResetDone(PasswordResetDoneView):
    template_name = 'main/password_reset_done.html'


class WebPasswordResetConfirm(PasswordResetConfirmView):
    template_name = 'main/password_reset_confirm.html'
    form_class = WebSetPasswordForm


class WebPasswordResetComplete(PasswordResetCompleteView):
    template_name = 'main/password_reset_complete.html'
    form_class = WebSetPasswordForm


def logout_user(request):
    logout(request)
    return redirect('home')


def add_player(request):
    if not request.user.is_superuser:
        return redirect('home')
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('players')
    else:
        form = PlayerForm()
    return render(request, 'main/Add_Player.html', {'form': form})


def players(request):
    plrs = Players.objects.filter(out=None).order_by('number')
    return render(request, 'main/Players.html', {'players': plrs})


def all_players(request):
    plrs = Players.objects.all().order_by('number')
    return render(request, 'main/Players.html', {'players': plrs})


def details_player(request, slug_player):
    plr = Players.objects.get(slug=slug_player)
    if AllGamesPlayers.objects.filter(player_id=plr.pk):
        agp = AllGamesPlayers.objects.get(player_id=plr.pk)
    else:
        agp = AllGamesPlayers.objects.filter(player_id=plr.pk)
    tb = Tables.objects.order_by('-start_date')[0]
    if TourGamesPlayers.objects.filter(player_id=plr.pk, table_id=tb.pk):
        tgp = TourGamesPlayers.objects.get(player_id=plr.pk, table_id=tb.pk)
    else:
        tgp = TourGamesPlayers.objects.filter(player_id=plr.pk, table_id=tb.pk)
    return render(request, 'main/Details_player.html', {'plr': plr, 'agp': agp, 'tgp': tgp})


def del_player(request, slug_player):
    if not request.user.is_superuser:
        return redirect('home')
    del_plr = Players.objects.get(slug=slug_player)
    del_plr.delete()
    return redirect('players')


class PlayerUpdateView(UpdateView):
    model = Players
    template_name = 'main/Upd_Player.html'
    form_class = PlayerForm

    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('home')
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)


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
    scr = Scoring.objects.filter(match_id=mtch.id).order_by('-score')
    count_scr = 0
    for s in scr:
        if s.score > 0:
            count_scr += 1

    if TransMatch.objects.filter(match_id=mtch.id):
        trans = TransMatch.objects.get(match_id=mtch.id)
        mtch_vt = MatchEvent.objects.filter(trans_id=trans.id).order_by('-timestamp')
        return render(request, 'main/StatsMatch.html', {
            'mtch': mtch,
            'scr': scr,
            'mtch_vt': mtch_vt,
            'trans': trans,
            'count': count_scr
        })
    return render(request, 'main/StatsMatch.html', {
        'mtch': mtch,
        'scr': scr,
        'count': count_scr
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


def del_match(request, slug_match):
    if not request.user.is_superuser:
        return redirect('home')
    m = Matches.objects.get(slug=slug_match)
    m.delete()
    return redirect('matches')


def live_match(request, slug_match):
    mtch = Matches.objects.get(slug=slug_match)
    if not TransMatch.objects.filter(match_id=mtch.id):
        TransMatch.objects.create(match=mtch)
    user = mark_safe(json.dumps(''))
    if request.user.is_authenticated:
        user = mark_safe(json.dumps(request.user.email))
    scr = Scoring.objects.filter(match_id=mtch.id).order_by('-score')
    count_scr = 0
    for s in scr:
        if s.score > 0:
            count_scr += 1

    trans = TransMatch.objects.get(match_id=mtch.id)
    timer = 'false'
    if (trans.start_1 and not trans.pause) or (trans.start_2 and not trans.end):
        timer = 'true'
    return render(request, 'main/Live_match.html', {
        'mtch': mtch,
        'scr': scr,
        'username': user,
        'trans': trans,
        'timer': timer,
        'count': count_scr
    })


def table(request):
    table_str = TablesView.objects.all()
    return render(request, 'main/Table.html', {'table_str': table_str})


def achievements(request):
    return render(request, 'main/Achievements.html')


def stats_team(request):
    agp = AllGamesPlayers.objects.all()
    return render(request, 'main/StatsTeam.html', {'agp': agp})
