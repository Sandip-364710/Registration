# Generated by Django 5.0.6 on 2024-07-02 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0003_remove_userinfo_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='skills',
            field=models.CharField(max_length=300),
        ),
    ]
