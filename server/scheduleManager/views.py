from django.shortcuts import render

from .models import IrrigationHour
from .models import ProgramStatus


def index(request):
    irrigation_hours = IrrigationHour.objects.all()

    print(ProgramStatus.objects.all())
    if (len(ProgramStatus.objects.all()) != 1):
        raise TypeError('Invalid dataset, ProgramStatus table not found')
    server_status = ProgramStatus.objects.all()[0]

    context = {'irrigation_hours': irrigation_hours,
               'server_status': server_status}

    return render(request, 'index.html', context)


