from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'scheduleManager'

urlpatterns = [
    path('', views.index, name='index'),
    path('submit_status', views.submit_status, name='submit_status'),
    path('submit_irrigation_hour', views.submit_irrigation_hour,
         name='submit_irrigation_hour'),
    url(r'^delete/(?P<pk>\d+)/$', views.irrigation_hour_delete,
        name='irrigation_hour_delete'),
    url(r'^ajax/submit_status/$', views.submit_status, name='submit_status'),
    url(r'^ajax/submit_cycle_settings/$', views.submit_cycle_settings,
        name='submit_cycle_settings'),
    url(r'^ajax/refresh_info/$', views.refresh_info,
        name='refresh_info')
]
