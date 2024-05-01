# Generated by Django 4.1.5 on 2023-01-26 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("monitor", "0023_rename_fibra_fiber"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dio",
            name="id",
            field=models.AutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="fiber",
            name="id",
            field=models.AutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="host",
            name="id",
            field=models.AutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="hostlog",
            name="id",
            field=models.AutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="port",
            name="id",
            field=models.AutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="portlog",
            name="id",
            field=models.AutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]