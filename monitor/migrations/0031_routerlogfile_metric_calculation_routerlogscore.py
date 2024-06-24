# Generated by Django 5.0.4 on 2024-06-21 09:55

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0030_routerlogfile_routerlog_logfile'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='routerlogfile',
            name='metric_calculation',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='RouterLogScore',
            fields=[
                ('pkid', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('traffic_voice_2g', models.FloatField(blank=True, null=True)),
                ('tchdrop', models.FloatField(blank=True, null=True)),
                ('sdcch_drop', models.FloatField(blank=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, default='', editable=False, max_length=25, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_createdby', to=settings.AUTH_USER_MODEL)),
                ('logfile', models.OneToOneField(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='monitor.routerlogfile')),
                ('modified_by', models.ForeignKey(blank=True, default='', editable=False, max_length=25, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_modifiedby', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created_on',),
                'abstract': False,
            },
        ),
    ]