from django.contrib import admin
from .models import IrrigationSlot
from .models import WeekDay
from .models import IrrigationHour
from .models import ProgramStatus
from .models import WeatherData


# Register your models here.
admin.site.register(IrrigationSlot)
admin.site.register(WeekDay)
admin.site.register(IrrigationHour)
admin.site.register(ProgramStatus)
admin.site.register(WeatherData)
