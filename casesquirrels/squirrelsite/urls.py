from django.urls import path

from . import views

app_name= 'squirrels'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('secret', views.SecretView.as_view(), name='secret'),
    path('newuser', views.signup, name='newuser'),
    path('redeem', views.RedeemView.as_view(), name='redeem'),
    path('leaderboard', views.LeaderboardView.as_view(), name='leaderboard'),
    path('cyoa', views.cyoa, name='cyoa'),
    path('article1', views.Article1View.as_view(), name='tree'),
    path('article2', views.Article2View.as_view(), name='tail'),
    path('article3', views.Article3View.as_view(), name='nuts'),
    path('article4', views.Article4View.as_view(), name='sqrl'),
    path('TAIL', views.TAIL, name='tail_layer'),
    path('TREE', views.TREE, name='tree_layer'),
    path('NUTS', views.NUTS, name='nuts_layer'),
    path('SQRL', views.SQRL, name='sqrl_layer'),
    path('chatter', views.chatter, name='chatter'),
]