# Generated by Django 5.0.6 on 2024-07-31 10:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0009_businessregistration_requiredexperience_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='businessregistration',
            name='requiredexperience',
        ),
    ]
