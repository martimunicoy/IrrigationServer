from django.db import models


class IrrigationSlot(models.Model):
    name = models.CharField(max_length=100)
    time_in_minutes = models.PositiveIntegerField(default=0)
    slot_id = models.AutoField(primary_key=True)

    class Meta:
        app_label = 'scheduleManager'
        ordering = ['slot_id',]
        db_table = 'irrigation_slots'

    def __str__(self):
        return 'Slot {:d}: {}'.format(self.slot_id, self.name)


class ProgramStatus(models.Model):
    running = models.BooleanField(default=False)
    testing = models.BooleanField(default=False)
    current_slot = models.PositiveIntegerField(default=0)

    class Meta:
        app_label = 'scheduleManager'
        db_table = 'program_status'


class WeekDay(models.Model):
    name = models.CharField(max_length=10)
    day_id = models.AutoField(primary_key=True)

    class Meta:
        app_label = 'scheduleManager'
        ordering = ['day_id',]
        db_table = 'week_days'

    def __str__(self):
        return self.name


class IrrigationHour(models.Model):
    hour = models.TimeField()
    week_days = models.ManyToManyField(WeekDay)
    hour_id = models.AutoField(primary_key=True)

    class Meta:
        app_label = 'scheduleManager'
        ordering = ['hour_id',]
        db_table = 'irrigation_hours'

    def __str__(self):
        return str(self.hour)
