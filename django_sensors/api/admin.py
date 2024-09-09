from django.contrib import admin

from .models import SensorType, SensorData, Metric, MetricEntry

# Register your models here.
admin.site.register(SensorType)
admin.site.register(SensorData)
admin.site.register(Metric)
admin.site.register(MetricEntry)