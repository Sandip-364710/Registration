# Generated by Django 5.0.6 on 2024-07-02 07:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_userinfo_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='username',
        ),
    ]
