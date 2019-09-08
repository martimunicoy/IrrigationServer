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


WD_DICT = {'Monday': 1,
           'Tuesday': 2,
           'Wednesday': 3,
           'Thursday': 4,
           'Friday': 5,
           'Saturday': 6,
           'Sunday': 7}

WD_DICT_R = {1: 'Monday',
             2: 'Tuesday',
             3: 'Wednesday',
             4: 'Thursday',
             5: 'Friday',
             6: 'Saturday',
             7: 'Sunday'}

class IrrigationHour(models.Model):
    hour = models.TimeField()
    week_days = models.ManyToManyField(WeekDay)
    hour_id = models.AutoField(primary_key=True)

    class Meta:
        app_label = 'scheduleManager'
        ordering = ['hour_id',]
        db_table = 'irrigation_hours'

    def print_weekdays_interval(self):
        indexes_list = []
        for wd in self.week_days.all():
            indexes_list.append(WD_DICT[wd.name])

        indexes_list.sort()

        old_i = -1
        n_neighbors = [0,] * 7

        for i in indexes_list:
            if (i == old_i + 1):
                n_neighbors[old_i - 1] += 1
                n_neighbors[i - 1] += 1
            old_i = i

        out = ''

        for j, i in enumerate(indexes_list):
            if (n_neighbors[i - 1] == 2):
                continue

            if (n_neighbors[i - 1] == 1):
                if (i > 1):
                    if (i < 7):
                        if (n_neighbors[i - 2] == 0):
                            out += WD_DICT_R[i]
                            if (n_neighbors[i] == 2):
                                out += '-'
                        else:
                            out += WD_DICT_R[i]
                    else:
                        out += WD_DICT_R[i]
                else:
                    out += WD_DICT_R[i]
                    if (n_neighbors[i] == 2):
                        out += '-'

            if (n_neighbors[i - 1] == 0):
                out += WD_DICT_R[i]

            if (j < len(indexes_list) - 1):
                if (out[-1] != '-'):
                    out += ', '

        return out

    def __str__(self):
        return '{}: {}'.format(self.print_weekdays_interval(), self.hour)
