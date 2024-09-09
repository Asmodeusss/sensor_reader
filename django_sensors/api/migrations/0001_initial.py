# Generated by Django 5.1 on 2024-09-08 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Metric',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('M_ID', models.IntegerField(default=0)),
                ('Name', models.CharField(max_length=200)),
                ('units', models.JSONField(default={})),
                ('Selected_id', models.IntegerField(default=0)),
                ('Selected_name', models.TextField()),
                ('Selected_precision', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='MetricEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Sensor_ID', models.IntegerField(default=0)),
                ('M_ID', models.CharField(max_length=20)),
                ('T', models.IntegerField(default=0)),
                ('V', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='SensorData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Sensor_ID', models.IntegerField(default=0)),
                ('Sensor_Type', models.IntegerField(default=0)),
                ('Sensor_Variant', models.IntegerField(default=0)),
                ('Sensor_Name', models.CharField(max_length=200)),
                ('Sensor_Metrics', models.JSONField(default={})),
            ],
        ),
        migrations.CreateModel(
            name='SensorType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('S_Id', models.PositiveIntegerField(default=0)),
                ('S_Variant', models.PositiveBigIntegerField(default=0)),
                ('S_Name', models.CharField(max_length=200)),
            ],
        ),
    ]
