from django.urls import path
from . import views
from .views import Registration, SingIn, NewsUpdateView

urlpatterns = [
    path('', views.home, name='home'),
    path('singIn', SingIn.as_view(), name='singIn'),
    path('logout', views.logout_user, name='logout'),
    path('registration', Registration.as_view(), name='registration'),
    path('news', views.all_news, name='all_news'),
    path('news/<slug:news_slug>', views.news, name='news'),
    path('add_new', views.add_new, name='add_new'),
    path('news/<slug:slug>/upd_new', NewsUpdateView.as_view(), name='upd_new'),
    path('news/<str:id_news>/del_new', views.del_new, name='del_new'),
    path('history', views.history, name='history'),
    path('achievements', views.achievements, name='achievements'),
    path('players', views.players, name='players'),
    path('players/<slug:slug_player>', views.details_player, name='details_player'),
    path('matches', views.matches, name='matches'),
    path('table', views.table, name='table'),
]
