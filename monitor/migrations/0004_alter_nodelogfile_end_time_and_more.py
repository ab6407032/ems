# Generated by Django 5.0.4 on 2024-08-14 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0003_remove_nodelogfile_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nodelogfile',
            name='end_time',
            field=models.DateTimeField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='nodelogfile',
            name='start_time',
            field=models.DateTimeField(blank=True, default='', null=True),
        ),
    ]