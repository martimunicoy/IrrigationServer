# Generated by Django 2.2.5 on 2020-05-22 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduleManager', '0010_programstatus_next_program_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='programstatus',
            name='next_program_delay',
        ),
        migrations.RemoveField(
            model_name='programstatus',
            name='next_program_description',
        ),
        migrations.AddField(
            model_name='programstatus',
            name='next_program_hour',
            field=models.TimeField(default=None),
        ),
    ]
