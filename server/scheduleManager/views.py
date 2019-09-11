from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages

from .models import IrrigationHour
from .models import ProgramStatus
from .forms import StatusUpdaterForm


def index(request):
    irrigation_hours = IrrigationHour.objects.all()

    if (len(ProgramStatus.objects.all()) != 1):
        raise TypeError('Invalid dataset, ProgramStatus table not found')
    server_status = ProgramStatus.objects.all()[0]

    status_updater_form = StatusUpdaterForm(initial={'current_slot': server_status.current_slot,
                                                  'running': server_status.running})
    context = {'irrigation_hours': irrigation_hours,
               'status_updater_form': status_updater_form}

    return render(request, 'index.html', context)


def submit_status(request):
    if (request.method == 'POST'):
        status_updater_form = StatusUpdaterForm(request.POST)
        if (status_updater_form.is_valid()):
            if (len(ProgramStatus.objects.all()) != 1):
                raise TypeError('Invalid dataset, ProgramStatus table not found')

            server_status = ProgramStatus.objects.all()[0]

            if (server_status.running != status_updater_form.cleaned_data['running']):
                messages.success(request, 'Irrigation program has {} successfully'.format(('started', 'ended')[int(status_updater_form.cleaned_data['running'] is False)]))
                server_status.running = status_updater_form.cleaned_data['running']

            if (server_status.current_slot != status_updater_form.cleaned_data['current_slot']):
                messages.success(request, 'Slot has been changed successfully')
                server_status.current_slot = status_updater_form.cleaned_data['current_slot']

            server_status.save()

    return HttpResponseRedirect('/scheduleManager/')