from django.urls import path
from . import views
from .views import Registration, SingIn

urlpatterns = [
    path('', views.home, name='home'),
    path('singIn', SingIn.as_view(), name='singIn'),
    path('logout', views.logout_user, name='logout'),
    path('registration', Registration.as_view(), name='registration'),
    path('history', views.history, name='history'),
    path('players', views.players, name='players'),
    path('matches', views.matches, name='matches'),
    path('table', views.table, name='table'),
]
