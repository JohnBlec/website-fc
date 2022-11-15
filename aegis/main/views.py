from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .forms import RegistrationForm, SingInForm
from .models import Players
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


def match(request):
    return render(request, 'main/Match.html')


def table(request):
    return render(request, 'main/Table.html')