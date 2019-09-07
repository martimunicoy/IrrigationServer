from django.urls import path

from . import views

app_name = 'scheduleManager'

urlpatterns = [
    path('', views.index, name='index'),
]

