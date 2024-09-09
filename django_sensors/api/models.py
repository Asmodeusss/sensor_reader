from django.db import models

# Create your models here.
class SensorType(models.Model):
    S_Id = models.PositiveIntegerField(default=0)
    S_Variant = models.PositiveBigIntegerField(default=0)
    S_Name = models.CharField(max_length=200)

    def __str__(self):
        return str(self.S_Id) + "_" + str(self.S_Variant) + "_" + str(self.S_Name)
    
class SensorData(models.Model):
    Sensor_ID = models.IntegerField(default=0)
    Sensor_Type = models.IntegerField(default=0)
    Sensor_Variant = models.IntegerField(default=0)
    Sensor_Name = models.CharField(max_length=200)

    Sensor_Metrics= models.JSONField(default=dict())

    def __str__(self):
        return str(self.Sensor_ID) + "_" + str(self.Sensor_Type) + "_" + str(self.Sensor_Name)

class Metric(models.Model):
    M_ID = models.IntegerField(default=0)
    Name = models.CharField(max_length=200)

    units = models.JSONField(default=dict())
    
    Selected_id = models.IntegerField(default=0)
    Selected_name = models.TextField()
    Selected_precision = models.FloatField(default=0)

    def __str__(self):
        return str(self.Selected_id) + "_" + str(self.Name)

class MetricEntry(models.Model):
    Sensor_ID = models.IntegerField(default=0)
    M_ID = models.CharField(max_length=20)
    T = models.IntegerField(default=0)
    V = models.FloatField(default=0.0)

    def __str__(self):
        return str(self.Sensor_ID) + "_" + str(self.M_ID)