# Generated by Django 2.2.5 on 2020-05-17 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduleManager', '0003_cyclesettings'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cyclesettings',
            name='slot6_active',
        ),
        migrations.AddField(
            model_name='cyclesettings',
            name='slot1_description',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='cyclesettings',
            name='slot2_description',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='cyclesettings',
            name='slot3_description',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='cyclesettings',
            name='slot4_description',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='cyclesettings',
            name='slot5_description',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='cyclesettings',
            name='slot6_description',
            field=models.TextField(default=''),
        ),
    ]
