# Generated by Django 5.0.7 on 2024-08-07 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APrimeApp', '0009_workshop_total_seats'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='attendance',
            field=models.TextField(blank=True, null=True),
        ),
    ]
