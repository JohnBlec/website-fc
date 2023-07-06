from django.contrib.auth.views import PasswordResetCompleteView
from django.urls import path
from . import views
from .views import Registration, SingIn, NewsUpdateView, PlayerUpdateView, WebPasswordReset, WebPasswordResetDone, \
    WebPasswordResetConfirm, WebPasswordResetComplete

urlpatterns = [
    path('', views.home, name='home'),
    path('singIn', SingIn.as_view(), name='singIn'),
    path('logout', views.logout_user, name='logout'),
    path('registration', Registration.as_view(), name='registration'),
    path("password_reset", WebPasswordReset.as_view(), name="password_reset"),
    path("password_reset/done/", WebPasswordResetDone.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", WebPasswordResetConfirm.as_view(), name="password_reset_confirm"),
    path("reset/done/", WebPasswordResetComplete.as_view(), name="password_reset_complete"),
    path('news', views.all_news, name='all_news'),
    path('news/add_new', views.add_new, name='add_new'),
    path('news/<slug:news_slug>', views.news, name='news'),
    path('news/<slug:slug>/upd_new', NewsUpdateView.as_view(), name='upd_new'),
    path('news/<str:id_news>/del_new', views.del_new, name='del_new'),
    path('history', views.history, name='history'),
    path('achievements', views.achievements, name='achievements'),
    path('stats_team', views.stats_team, name='stats_team'),
    path('players', views.players, name='players'),
    path('players/all', views.all_players, name='all_players'),
    path('players/add_player', views.add_player, name='add_player'),
    path('players/<slug:slug_player>', views.details_player, name='details_player'),
    path('players/<slug:slug_player>/del_player', views.del_player, name='del_player'),
    path('players/<slug:slug>/upd_player', PlayerUpdateView.as_view(), name='upd_player'),
    path('matches', views.matches, name='matches'),
    path('matches/all_matches', views.all_matches, name='all_matches'),
    path('matches/add_match', views.add_match, name='add_match'),
    path('matches/<slug:slug>/upd_match', views.MatchUpdateView.as_view(), name='upd_match'),
    path('matches/<slug:slug_match>/editor_scoring', views.editor_scoring, name='editor_scoring'),
    path('matches/<slug:slug_match>/editor_scoring/<str:id_scoring>/del_scoring', views.del_scoring, name='del_scoring'),
    path('matches/<str:slug_match>/del_match', views.del_match, name='del_match'),
    path('matches/<slug:slug_match>', views.match, name='match'),
    path('matches/<slug:slug_match>/live', views.live_match, name='live_match'),
    path('table', views.table, name='table'),
]
