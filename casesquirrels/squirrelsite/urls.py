from django.urls import path

from . import views

app_name= 'squirrels'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('secret', views.SecretView.as_view(), name='secret'),
    path('newuser', views.signup, name='newuser'),
]