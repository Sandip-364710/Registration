# Generated by Django 5.0.6 on 2024-07-02 13:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0007_rename_username_userinfo_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='name',
        ),
    ]
