from django.urls import path

from . import views

app_name = 'scheduleManager'

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('submit_status', views.submit_status, name='submit_status')
]

