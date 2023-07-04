from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import *


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Account
        fields = ('email', 'password1', 'password2')


class SingInForm(AuthenticationForm):
    username = forms.CharField(label='Email', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class AddNewForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'slug', 'short_description', 'content', 'img', 'publisher']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'slug': forms.TextInput(attrs={'class': 'form-input'}),
            'short_description': forms.Textarea(attrs={'cols': 60, 'rows': 5}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }


class PlayerForm(forms.ModelForm):
    class Meta:
        model = Players
        fields = ['slug', 'first_name', 'last_name', 'number',
                  'characteristic', 'birthday',
                  'signed', 'out',
                  'link_vk', 'photo']


class MatchForm(forms.ModelForm):
    class Meta:
        model = Matches
        fields = ['slug', 'date', 'stage', 'table_tournament',
                  'home_team', 'away_team',
                  'home_goals', 'away_goals',
                  'link_vk']
        widgets = {
            'slug': forms.TextInput(attrs={'class': 'form-input'}),
            'date': forms.DateInput(),
            'stage': forms.TextInput(attrs={'class': 'form-input'}),
            'link_vk': forms.TextInput(attrs={'class': 'form-input'}),
        }


class ScoringForm(forms.ModelForm):
    class Meta:
        model = Scoring
        fields = ['player', 'score']


class ScoreForm(forms.ModelForm):
    class Meta:
        model = Scoring
        fields = ['player', 'score']
