from django.contrib import admin
from .models import Players
from .models import Tournaments

admin.site.register(Players)
admin.site.register(Tournaments)