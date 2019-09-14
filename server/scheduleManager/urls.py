from django.urls import path

from . import views

app_name = 'scheduleManager'

urlpatterns = [
    path('', views.index, name='index'),
    path('submit_status', views.submit_status, name='submit_status'),
    path('delete/(?P<pk>[0-9]+)', views.irrigation_hour_delete,
         name='irrigation_hour_delete')
]
