# Generated by Django 2.1 on 2018-08-09 19:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0006_auto_20180809_1109'),
    ]

    operations = [
        migrations.AddField(
            model_name='portlog',
            name='host',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='monitor.Host'),
        ),
    ]
