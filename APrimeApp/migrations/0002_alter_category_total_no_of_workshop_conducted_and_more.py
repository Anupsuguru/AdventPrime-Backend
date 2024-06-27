# Generated by Django 5.0.6 on 2024-06-27 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APrimeApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='total_no_of_workshop_conducted',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='department',
            name='total_no_of_workshop_conducted',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='resource',
            field=models.TextField(blank=True, null=True),
        ),
    ]
