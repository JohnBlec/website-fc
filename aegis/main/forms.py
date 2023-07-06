from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django import forms
from .models import *
from django.utils.translation import gettext_lazy as _


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


class WebPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email", 'class': 'form-control'}),
    )


class WebSetPasswordForm(SetPasswordForm):
    error_messages = {
        "password_mismatch": _("The two password fields didn’t match."),
    }
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class': 'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class': 'form-control'}),
    )


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
