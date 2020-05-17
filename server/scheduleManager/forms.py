from django import forms
from django.forms import widgets

from .models import WeekDay


class StatusUpdaterForm(forms.Form):
    running = forms.BooleanField(required=False)
    current_slot = forms.DecimalField(
        label='', max_value=6, min_value=1, max_digits=1, decimal_places=0,
        required=False)


class IrrigationHourForm(forms.Form):
    hour = forms.DecimalField(label='', max_value=23, min_value=0,
                              max_digits=2, decimal_places=0, required=True)
    minute = forms.DecimalField(label='', max_value=59, min_value=0,
                                max_digits=2, decimal_places=0, required=True)
    week_day = forms.ModelMultipleChoiceField(
        queryset=WeekDay.objects.all(),
        required=True,
        widget=widgets.CheckboxSelectMultiple(
            attrs={'class': 'week_days_selector'}))


class CycleSettingsForm(forms.Form):
    slot1_time = forms.DecimalField(min_value=0, decimal_places=0,
                                    required=True, max_digits=3)
    slot2_time = forms.DecimalField(min_value=0, decimal_places=0,
                                    required=True, max_digits=3)
    slot3_time = forms.DecimalField(min_value=0, decimal_places=0,
                                    required=True, max_digits=3)
    slot4_time = forms.DecimalField(min_value=0, decimal_places=0,
                                    required=True, max_digits=3)
    slot5_time = forms.DecimalField(min_value=0, decimal_places=0,
                                    required=True, max_digits=3)
    slot6_time = forms.DecimalField(min_value=0, decimal_places=0,
                                    required=True, max_digits=3)
    slot1_active = forms.BooleanField(required=False)
    slot2_active = forms.BooleanField(required=False)
    slot3_active = forms.BooleanField(required=False)
    slot4_active = forms.BooleanField(required=False)
    slot5_active = forms.BooleanField(required=False)
    slot6_active = forms.BooleanField(required=False)
    slot1_description = forms.CharField(required=False)
    slot2_description = forms.CharField(required=False)
    slot3_description = forms.CharField(required=False)
    slot4_description = forms.CharField(required=False)
    slot5_description = forms.CharField(required=False)
    slot6_description = forms.CharField(required=False)
