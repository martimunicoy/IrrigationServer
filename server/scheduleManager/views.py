from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.contrib import messages

import json
import datetime

from .models import IrrigationHour
from .models import ProgramStatus
from .models import CycleSettings
from .forms import StatusUpdaterForm
from .forms import IrrigationHourForm
from .forms import CycleSettingsForm
from . import graphs


def index(request):
    info = ProgramStatus.objects.all()[0]
    irrigation_hours = IrrigationHour.objects.all()

    if (len(ProgramStatus.objects.all()) != 1):
        raise TypeError('Invalid dataset, ProgramStatus table not found')
    server_status = ProgramStatus.objects.all()[0]
    cycle_settings = CycleSettings.objects.all()[0]

    if server_status.manual:
        status_update_form_initial = {'manual': 1}
    else:
        status_update_form_initial = {'manual': 0}

    status_updater_form = StatusUpdaterForm(
        initial=status_update_form_initial)

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

    context = {'info': info,
               'irrigation_hours': irrigation_hours,
               'status_updater_form': status_updater_form,
               'irrigation_hour_form': irrigation_hour_form,
               'cycle_settings_form': cycle_settings_form,
               'plot_div': plt_div}

    return render(request, 'index.html', context)


def handle_messages(request, response_data=None):
    if response_data is None:
        response_data = {}

    django_messages = []
    for message in messages.get_messages(request):
        django_messages.append({"message": message.message})

    response_data['messages'] = django_messages

    return response_data


def refresh_info(request):
    info = ProgramStatus.objects.all()[0]

    response_data = {}
    response_data['running'] = info.running_state
    response_data['manual'] = info.manual_state
    response_data['slot_num'] = info.current_slot
    response_data['slot_desc'] = info.slot_description

    return HttpResponse(json.dumps(response_data),
                        content_type="application/json")


def submit_status(request):
    if request.method == 'POST':
        manual = json.loads(request.POST.get('manual'))
        running = json.loads(request.POST.get('running'))
        try:
            current_slot = int(request.POST.get('current_slot'))
        except ValueError:
            current_slot = None

        server_status = ProgramStatus.objects.all()[0]

        if manual != server_status.manual:
            messages.success(request,
                             'Mode {} '.format(('automàtic', 'manual')
                                               [manual == True]) + 'establert')

        if manual == 0:  # automatic mode
            server_status.manual = False
        else:  # manual mode
            server_status.manual = True

            if (server_status.running != running):
                messages.success(
                    request,
                    'El rec s\'ha {} satisfactòriament'.format(
                        ('obert', 'tancat')[int(running is False)]))
                server_status.running = running

            if (current_slot is not None
                    and server_status.current_slot != current_slot):
                messages.success(request, 'Posició canviada satisfactòriament')
                server_status.current_slot = current_slot

        server_status.save()

        response_data = handle_messages(request)

        return HttpResponse(json.dumps(response_data),
                            content_type="application/json")
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


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
        slot1_description = str(request.POST.get('slot1_description'))
        slot1_active = json.loads(request.POST.get('slot1_active'))
        slot1_time = int(request.POST.get('slot1_time'))

        slot2_description = str(request.POST.get('slot2_description'))
        slot2_active = json.loads(request.POST.get('slot2_active'))
        slot2_time = int(request.POST.get('slot2_time'))

        slot3_description = str(request.POST.get('slot3_description'))
        slot3_active = json.loads(request.POST.get('slot3_active'))
        slot3_time = int(request.POST.get('slot3_time'))

        slot4_description = str(request.POST.get('slot4_description'))
        slot4_active = json.loads(request.POST.get('slot4_active'))
        slot4_time = int(request.POST.get('slot4_time'))

        slot5_description = str(request.POST.get('slot5_description'))
        slot5_active = json.loads(request.POST.get('slot5_active'))
        slot5_time = int(request.POST.get('slot5_time'))

        slot6_description = str(request.POST.get('slot6_description'))
        slot6_active = json.loads(request.POST.get('slot6_active'))
        slot6_time = int(request.POST.get('slot6_time'))

        cycle_settings = CycleSettings.objects.all()[0]

        changes = []
        if (cycle_settings.slot1_description != slot1_description):
            changes.append('Descripció de la posició 1')
            cycle_settings.slot1_description = slot1_description

        if (cycle_settings.slot1_active != slot1_active):
            changes.append('Activació de la posició 1')
            cycle_settings.slot1_active = slot1_active

        if (cycle_settings.slot1_time != slot1_time):
            changes.append('Temps de rec de la posició 1')
            cycle_settings.slot1_time = slot1_time

        if (cycle_settings.slot2_description != slot2_description):
            changes.append('Descripció de la posició 2')
            cycle_settings.slot2_description = slot2_description

        if (cycle_settings.slot2_active != slot2_active):
            changes.append('Activació de la posició 2')
            cycle_settings.slot2_active = slot2_active

        if (cycle_settings.slot2_time != slot2_time):
            changes.append('Temps de rec de la posició 2')
            cycle_settings.slot2_time = slot2_time

        if (cycle_settings.slot3_description != slot3_description):
            changes.append('Descripció de la posició 3')
            cycle_settings.slot3_description = slot3_description

        if (cycle_settings.slot3_active != slot3_active):
            changes.append('Activació de la posició 3')
            cycle_settings.slot3_active = slot3_active

        if (cycle_settings.slot3_time != slot3_time):
            changes.append('Temps de rec de la posició 3')
            cycle_settings.slot3_time = slot3_time

        if (cycle_settings.slot4_description != slot4_description):
            changes.append('Descripció de la posició 4')
            cycle_settings.slot4_description = slot4_description

        if (cycle_settings.slot4_active != slot4_active):
            changes.append('Activació de la posició 4')
            cycle_settings.slot4_active = slot4_active

        if (cycle_settings.slot4_time != slot4_time):
            changes.append('Temps de rec de la posició 4')
            cycle_settings.slot4_time = slot4_time

        if (cycle_settings.slot5_description != slot5_description):
            changes.append('Descripció de la posició 5')
            cycle_settings.slot5_description = slot5_description

        if (cycle_settings.slot5_active != slot5_active):
            changes.append('Activació de la posició 5')
            cycle_settings.slot5_active = slot5_active

        if (cycle_settings.slot5_time != slot5_time):
            changes.append('Temps de rec de la posició 5')
            cycle_settings.slot5_time = slot5_time

        if (cycle_settings.slot6_description != slot6_description):
            changes.append('Descripció de la posició 6')
            cycle_settings.slot6_description = slot6_description

        if (cycle_settings.slot6_active != slot6_active):
            changes.append('Activació de la posició 6')
            cycle_settings.slot6_active = slot6_active

        if (cycle_settings.slot6_time != slot6_time):
            changes.append('Temps de rec de la posició 6')
            cycle_settings.slot6_time = slot6_time

        for change in changes:
            if 'Temps' in change:
                messages.success(request, change
                                 + ' actualitzat satisfactòriament')
            else:
                messages.success(request, change
                                 + ' actualitzada satisfactòriament')

        response_data = handle_messages(request)

        cycle_settings.save()

        return HttpResponse(json.dumps(response_data),
                            content_type="application/json")
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


def irrigation_hour_delete(request, pk):
    irrigation_hour = get_object_or_404(IrrigationHour, pk=pk)

    if request.method == 'POST':
        irrigation_hour.delete()

        messages.success(request, 'Programa eliminat satisfactòriament')

    return HttpResponseRedirect('/scheduleManager/')
