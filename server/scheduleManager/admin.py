from django.contrib import admin
from .models import IrrigationSlot
from .models import WeekDay
from .models import IrrigationHour
from .models import ProgramStatus
from .models import WeatherData
from .models import CycleSettings


# Register your models here.
admin.site.register(IrrigationSlot)
admin.site.register(WeekDay)
admin.site.register(IrrigationHour)
admin.site.register(ProgramStatus)
admin.site.register(WeatherData)
admin.site.register(CycleSettings)
