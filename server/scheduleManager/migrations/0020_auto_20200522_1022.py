# Generated by Django 2.2.5 on 2020-05-22 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduleManager', '0019_auto_20200522_1014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='programstatus',
            name='next_program_hour',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]