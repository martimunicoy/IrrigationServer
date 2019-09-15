from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'scheduleManager'

urlpatterns = [
    path('', views.index, name='index'),
    path('submit_status', views.submit_status, name='submit_status'),
    url(r'^delete/(?P<pk>\d+)/$', views.irrigation_hour_delete,
        name='irrigation_hour_delete')
]
