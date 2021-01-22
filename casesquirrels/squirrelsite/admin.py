from django.contrib import admin

# Register your models here.
from .models import Score, Merch, Puzzle, Redeemed

admin.site.register(Puzzle)
admin.site.register(Merch)
admin.site.register(Score)
admin.site.register(Redeemed)