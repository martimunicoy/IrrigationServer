from django.db import models


class IrrigationSlot(models.Model):
    name = models.CharField(max_length=100)
    time_in_minutes = models.PositiveIntegerField(default=0)
    slot_id = models.AutoField(primary_key=True)

    class Meta:
        app_label = 'scheduleManager'
        ordering = ['slot_id', ]
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

    @property
    def running_state(self):
        if self.running:
            return 'obert'
        else:
            return 'tancat'

    @property
    def slot_description(self):
        cycle_settings = CycleSettings.objects.all()[0]
        return cycle_settings.get_description(self.current_slot)


class CycleSettings(models.Model):
    slot1_time = models.PositiveIntegerField(default=60)
    slot2_time = models.PositiveIntegerField(default=60)
    slot3_time = models.PositiveIntegerField(default=60)
    slot4_time = models.PositiveIntegerField(default=60)
    slot5_time = models.PositiveIntegerField(default=60)
    slot6_time = models.PositiveIntegerField(default=60)
    slot1_active = models.BooleanField(default=True)
    slot2_active = models.BooleanField(default=True)
    slot3_active = models.BooleanField(default=True)
    slot4_active = models.BooleanField(default=True)
    slot5_active = models.BooleanField(default=True)
    slot6_active = models.BooleanField(default='')
    slot1_description = models.TextField(default='')
    slot2_description = models.TextField(default='')
    slot3_description = models.TextField(default='')
    slot4_description = models.TextField(default='')
    slot5_description = models.TextField(default='')
    slot6_description = models.TextField(default='')

    class Meta:
        app_label = 'scheduleManager'
        db_table = 'cycle_settings'

    def get_description(self, slot_id):
        if (slot_id == 1):
            return self.slot1_description
        elif (slot_id == 2):
            return self.slot2_description
        elif (slot_id == 3):
            return self.slot3_description
        elif (slot_id == 4):
            return self.slot4_description
        elif (slot_id == 5):
            return self.slot5_description
        elif (slot_id == 6):
            return self.slot6_description
        else:
            return 'Desconegut'


class WeekDay(models.Model):
    name = models.CharField(max_length=10)
    day_id = models.AutoField(primary_key=True)

    class Meta:
        app_label = 'scheduleManager'
        ordering = ['day_id', ]
        db_table = 'week_days'

    def to_catalan(func):
        def wrapper(*args):
            english_weekdays = func(*args)
            catalan_weekdays = english_weekdays.replace('Monday', 'Dilluns')
            catalan_weekdays = catalan_weekdays.replace('Tuesday', 'Dimarts')
            catalan_weekdays = catalan_weekdays.replace(
                'Wednesday', 'Dimecres')
            catalan_weekdays = catalan_weekdays.replace('Thursday', 'Dijous')
            catalan_weekdays = catalan_weekdays.replace('Friday', 'Divendres')
            catalan_weekdays = catalan_weekdays.replace('Saturday', 'Dissabte')
            catalan_weekdays = catalan_weekdays.replace('Sunday', 'Diumenge')
            return catalan_weekdays
        return wrapper

    @to_catalan
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
        ordering = ['hour_id', ]
        db_table = 'irrigation_hours'

    def to_catalan(func):
        def wrapper(*args):
            english_weekdays = func(*args)
            catalan_weekdays = english_weekdays.replace('Monday', 'Dilluns')
            catalan_weekdays = catalan_weekdays.replace('Tuesday', 'Dimarts')
            catalan_weekdays = catalan_weekdays.replace(
                'Wednesday', 'Dimecres')
            catalan_weekdays = catalan_weekdays.replace('Thursday', 'Dijous')
            catalan_weekdays = catalan_weekdays.replace('Friday', 'Divendres')
            catalan_weekdays = catalan_weekdays.replace('Saturday', 'Dissabte')
            catalan_weekdays = catalan_weekdays.replace('Sunday', 'Diumenge')
            return catalan_weekdays
        return wrapper

    def get_week_days(self):
        return self.week_days

    @to_catalan
    def print_weekdays_interval(self):
        indexes_list = []
        for wd in self.week_days.all():
            indexes_list.append(WD_DICT[wd.name])

        indexes_list.sort()

        old_i = -1
        n_neighbors = [0, ] * 7

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
        return '{}: {:02d}h{:02d}'.format(self.print_weekdays_interval(),
                                          self.hour.hour, self.hour.minute)


class WeatherData(models.Model):
    datetime = models.DateTimeField()
    rain_intensity = models.FloatField()

    class Meta:
        app_label = 'scheduleManager'
        ordering = ['datetime', ]
        db_table = 'weather_data'
