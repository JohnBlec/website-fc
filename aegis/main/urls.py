from django.urls import path
from . import views
from .views import Registration, SingIn

urlpatterns = [
    path('', views.home, name='home'),
    path('singIn', SingIn.as_view(), name='singIn'),
    path('logout', views.logout_user, name='logout'),
    path('registration', Registration.as_view(), name='registration'),
    path('news', views.all_news, name='all_news'),
    path('news/<slug:news_slug>', views.news, name='news'),
    path('add_new', views.add_new, name='add_new'),
    path('del_new/<str:id_news>', views.del_new, name='del_new'),
    path('history', views.history, name='history'),
    path('achievements', views.achievements, name='achievements'),
    path('players', views.players, name='players'),
    path('matches', views.matches, name='matches'),
    path('table', views.table, name='table'),
]
