# Generated by Django 3.2.8 on 2022-01-10 14:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_booking_booked_on'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hotel',
            name='description',
        ),
    ]
