# Generated by Django 5.0.4 on 2024-06-21 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0034_alter_routerlogscore_sdcch_drop_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='routerlogfile',
            name='sdcch_drop',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='routerlogfile',
            name='tchdrop',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='routerlogfile',
            name='traffic_voice_2g',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
