# Generated by Django 5.0.6 on 2024-07-31 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0008_remove_userinfo_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='businessregistration',
            name='requiredexperience',
            field=models.CharField( max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='businessregistration',
            name='salary',
            field=models.CharField(default='exit', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='businessregistration',
            name='skills',
            field=models.TextField(default='exit', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='businessregistration',
            name='city',
            field=models.CharField(default='exit', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='businessregistration',
            name='state',
            field=models.CharField(default='exit', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='businessregistration',
            name='website',
            field=models.CharField(default='exit', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='individualregistration',
            name='experience',
            field=models.CharField(default='exit', max_length=255),
            preserve_default=False,
        ),
    ]
