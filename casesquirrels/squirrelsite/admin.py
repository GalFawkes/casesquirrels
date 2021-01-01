from django.contrib import admin

# Register your models here.
from .models import Score, Merch, Puzzle

admin.site.register(Puzzle)
admin.site.register(Merch)
admin.site.register(Score)