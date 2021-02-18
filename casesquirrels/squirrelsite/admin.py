from django.contrib import admin

# Register your models here.
from .models import Score, Merch, Puzzle, Redeemed, Squad, SquadMember

admin.site.register(Puzzle)
admin.site.register(Merch)
admin.site.register(Score)
admin.site.register(Redeemed)
admin.site.register(Squad)
admin.site.register(SquadMember)