# Generated by Django 5.0.6 on 2024-07-02 13:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0006_userinfo_username'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userinfo',
            old_name='username',
            new_name='name',
        ),
    ]
