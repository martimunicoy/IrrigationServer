# Generated by Django 2.2.5 on 2020-05-22 07:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduleManager', '0014_auto_20200522_0949'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='programstatus',
            name='next_program_hour',
        ),
    ]
