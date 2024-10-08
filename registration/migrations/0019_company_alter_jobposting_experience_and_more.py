# Generated by Django 5.0.6 on 2024-08-22 04:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0018_businessregistration_password_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterField(
            model_name='jobposting',
            name='experience',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='jobposting',
            name='skills',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='jobposting',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registration.company'),
        ),
    ]
