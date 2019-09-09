from django import forms

from .models import ProgramStatus

class StatusUpdaterForm(forms.Form):
    running = forms.BooleanField(required=False)
    current_slot = forms.DecimalField(label='', max_value=6, min_value=1, max_digits=1, decimal_places=0, required=False)
