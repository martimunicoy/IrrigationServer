# Generated by Django 2.2.5 on 2020-05-22 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduleManager', '0008_programstatus_next_program'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='programstatus',
            name='next_program',
        ),
        migrations.AddField(
            model_name='programstatus',
            name='next_program_delay',
            field=models.IntegerField(default=-1),
        ),
    ]
