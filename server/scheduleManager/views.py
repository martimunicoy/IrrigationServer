from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages

import datetime

from .models import IrrigationHour
from .models import ProgramStatus
from .models import CycleSettings
from .forms import StatusUpdaterForm
from .forms import IrrigationHourForm
from .forms import CycleSettingsForm
from . import graphs


def index(request):
    irrigation_hours = IrrigationHour.objects.all()

    if (len(ProgramStatus.objects.all()) != 1):
        raise TypeError('Invalid dataset, ProgramStatus table not found')
    server_status = ProgramStatus.objects.all()[0]
    cycle_settings = CycleSettings.objects.all()[0]

    status_updater_form = StatusUpdaterForm(
        initial={'current_slot': server_status.current_slot,
                 'running': server_status.running})

    irrigation_hour_form = IrrigationHourForm(
        initial={'hour': 0, 'minute': 0})

    cycle_settings_form = CycleSettingsForm(
        initial={'slot1_time': cycle_settings.slot1_time,
                 'slot2_time': cycle_settings.slot2_time,
                 'slot3_time': cycle_settings.slot3_time,
                 'slot4_time': cycle_settings.slot4_time,
                 'slot5_time': cycle_settings.slot5_time,
                 'slot6_time': cycle_settings.slot6_time,
                 'slot1_active': cycle_settings.slot1_active,
                 'slot2_active': cycle_settings.slot2_active,
                 'slot3_active': cycle_settings.slot3_active,
                 'slot4_active': cycle_settings.slot4_active,
                 'slot5_active': cycle_settings.slot5_active,
                 'slot6_active': cycle_settings.slot6_active,
                 'slot1_description': cycle_settings.slot1_description,
                 'slot2_description': cycle_settings.slot2_description,
                 'slot3_description': cycle_settings.slot3_description,
                 'slot4_description': cycle_settings.slot4_description,
                 'slot5_description': cycle_settings.slot5_description,
                 'slot6_description': cycle_settings.slot6_description})

    plt_div = graphs.create_schedule_graph(hour_range=24)

    context = {'irrigation_hours': irrigation_hours,
               'status_updater_form': status_updater_form,
               'irrigation_hour_form': irrigation_hour_form,
               'cycle_settings_form': cycle_settings_form,
               'plot_div': plt_div}

    return render(request, 'index.html', context)


def submit_status(request):
    if (request.method == 'POST'):
        status_updater_form = StatusUpdaterForm(request.POST)
        if (status_updater_form.is_valid()):
            if (len(ProgramStatus.objects.all()) != 1):
                raise TypeError('Invalid dataset, '
                                + 'ProgramStatus table not found')

            server_status = ProgramStatus.objects.all()[0]

            if (server_status.running
                    != status_updater_form.cleaned_data['running']):
                messages.success(
                    request, 'El rec s\'ha '
                    + '{} satisfactòriament'.format(
                        ('obert', 'tancat')
                        [int(status_updater_form.cleaned_data['running']
                             is False)]))
                server_status.running = \
                    status_updater_form.cleaned_data['running']

            if (server_status.current_slot
                    != status_updater_form.cleaned_data['current_slot']):
                messages.success(request, 'Posició canviada satisfactòriament')
                server_status.current_slot = \
                    status_updater_form.cleaned_data['current_slot']

            server_status.save()

    return HttpResponseRedirect('/scheduleManager/')


def submit_irrigation_hour(request):
    if (request.method == 'POST'):
        irrigation_hour_form = IrrigationHourForm(request.POST)
        if (irrigation_hour_form.is_valid()):

            time = datetime.time(
                hour=irrigation_hour_form.cleaned_data['hour'],
                minute=irrigation_hour_form.cleaned_data['minute'],
                second=0, microsecond=0)

            new_irrigation_hour = IrrigationHour(hour=time)

            new_irrigation_hour.save()

            for week_day in irrigation_hour_form.cleaned_data['week_day']:
                new_irrigation_hour.week_days.add(week_day)

            messages.success(request, 'Nou programa afegit satisfactòriament')
    return HttpResponseRedirect('/scheduleManager/')


def submit_cycle_settings(request):
    if (request.method == 'POST'):
        cycle_settings_form = CycleSettingsForm(request.POST)
        if (cycle_settings_form.is_valid()):

            cycle_settings = CycleSettings.objects.all()[0]

            cycle_settings.slot1_time = \
                cycle_settings_form.cleaned_data['slot1_time']

            cycle_settings.slot2_time = \
                cycle_settings_form.cleaned_data['slot2_time']

            cycle_settings.slot3_time = \
                cycle_settings_form.cleaned_data['slot3_time']

            cycle_settings.slot4_time = \
                cycle_settings_form.cleaned_data['slot4_time']

            cycle_settings.slot5_time = \
                cycle_settings_form.cleaned_data['slot5_time']

            cycle_settings.slot6_time = \
                cycle_settings_form.cleaned_data['slot6_time']

            cycle_settings.slot1_active = \
                cycle_settings_form.cleaned_data['slot1_active']

            cycle_settings.slot2_active = \
                cycle_settings_form.cleaned_data['slot2_active']

            cycle_settings.slot3_active = \
                cycle_settings_form.cleaned_data['slot3_active']

            cycle_settings.slot4_active = \
                cycle_settings_form.cleaned_data['slot4_active']

            cycle_settings.slot5_active = \
                cycle_settings_form.cleaned_data['slot5_active']

            cycle_settings.slot6_active = \
                cycle_settings_form.cleaned_data['slot6_active']

            cycle_settings.slot1_description = \
                cycle_settings_form.cleaned_data['slot1_description']

            cycle_settings.slot2_description = \
                cycle_settings_form.cleaned_data['slot2_description']

            cycle_settings.slot3_description = \
                cycle_settings_form.cleaned_data['slot3_description']

            cycle_settings.slot4_description = \
                cycle_settings_form.cleaned_data['slot4_description']

            cycle_settings.slot5_description = \
                cycle_settings_form.cleaned_data['slot5_description']

            cycle_settings.slot6_description = \
                cycle_settings_form.cleaned_data['slot6_description']

            cycle_settings.save()

            messages.success(request, 'Cicle configurat satisfactòriament')
    return HttpResponseRedirect('/scheduleManager/')


def irrigation_hour_delete(request, pk):
    irrigation_hour = get_object_or_404(IrrigationHour, pk=pk)

    if request.method == 'POST':
        irrigation_hour.delete()

        messages.success(request, 'Programa eliminat satisfactòriament')

    return HttpResponseRedirect('/scheduleManager/')
