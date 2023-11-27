from django.urls import path
from . import views

app_name = 'games'

urlpatterns = [
    path('slots/',views.slot,name='slot'),
    path('<int:bet>/spinning/', views.game, name='play'),
]
