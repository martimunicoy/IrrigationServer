# Generated by Django 2.2.5 on 2020-05-22 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduleManager', '0009_auto_20200522_0901'),
    ]

    operations = [
        migrations.AddField(
            model_name='programstatus',
            name='next_program_description',
            field=models.TextField(default='Desconegut'),
        ),
    ]