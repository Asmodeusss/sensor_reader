"""
URL configuration for django_sensors project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from os import listdir
from api.models import SensorType, SensorData, Metric, MetricEntry
from django.db import connection

import json
import codecs

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include("api.urls"))
]


printDebug = True

#this can autoload data from the json files if enabled, but may require changing around the directory used
if False:

    dirs = listdir("../data")

    all_tables = connection.introspection.table_names()

    print(all_tables)

    for dir in dirs:
        #sensor types
        if dir.lower().startswith("sensortypes") and ("api_sensortype" in all_tables):
            f = open("../data/" + dir)
            data = json.loads(f.read())
            
            if printDebug:
                print("")
                print("reading sensor type data: " + str(dir))

            for sensor_id in data:
                for sensor_type in data[sensor_id]:
                    sensor_name = data[sensor_id][sensor_type]["name"]

                    qry = SensorType.objects.filter(S_Id=sensor_id, S_Variant=sensor_type)
                    if (qry.exists()):
                        if printDebug: print("preexisting sensor in DB: " + sensor_name)
                    else:
                        sensor = SensorType()
                        sensor.S_Id = sensor_id
                        sensor.S_Variant = sensor_type
                        sensor.S_Name = sensor_name
                        sensor.save()
                        print(sensor_name + " instantiated ")
            f.close()

        #sensor readings
        if dir.lower().startswith("sensors") and ("api_sensordata" in all_tables) and ("api_metricentry" in all_tables):
            f = open("../data/" + dir)
            data = json.loads(f.read())
            
            if printDebug:
                print("reading sensor reading data: " + str(dir))
            for reading_id in data:
                sensor_metrics = data[reading_id]["metrics"]
                sensor_name = data[reading_id]["name"]
                sensor_type = data[reading_id]["type"]
                sensor_variant = data[reading_id]["variant"]

                if not sensor_name:
                    if printDebug: print("DATA ERROR: Sensor name for sensor " + str(reading_id) + " from file " + str(dir) + " is missing.")
                    sensor_name = "UNDEFINED"
                    #continue

                if not sensor_type:
                    if printDebug: print("DATA ERROR: Sensor type for sensor " + str(reading_id) + " from file " + str(dir) + " is missing.")
                    continue

                if not sensor_variant:
                    if printDebug: print("DATA ERROR: Sensor variant for sensor " + str(reading_id) + " from file " + str(dir) + " is missing.")
                    continue

                if not sensor_metrics:
                    if printDebug: print("DATA ERROR: Sensor data for sensor " + str(reading_id) + " from file " + str(dir) + " is missing.")
                    continue

                if not sensor_metrics:
                    if printDebug: print("DATA ERROR: Metrics data for sensor " + str(reading_id) + " from file " + str(dir) + " is missing.")
                    
                metrics_final = []
                for metric in sensor_metrics:
                    c_metric = sensor_metrics[metric]

                    if (metric == "5"):
                        print("metric is 5")

                    qry = MetricEntry.objects.filter(M_ID=metric, Sensor_ID=reading_id)
                    if qry.exists():
                        if printDebug: print("metric entry for " + str(reading_id) + " " + str(metric) + " in file " + str(dir) + " already present in DB.")
                        continue
                    
                    new_entry = MetricEntry()
                    new_entry.Sensor_ID = reading_id #confusing. in this case reading_id is the sensors id in the sensor file. Should have picked a better name.
                    new_entry.M_ID = metric
                    new_entry.T = c_metric["t"]
                    new_entry.V = c_metric["v"]
                    new_entry.save()
                    
 
                qry = SensorData.objects.filter(Sensor_ID=reading_id)
                if qry.exists():
                    if printDebug: print("DB entry for sensor " + str(sensor_name) + " from file " + dir + " is duplicate")
                    continue

                sensor = SensorData()
                sensor.Sensor_ID = reading_id
                sensor.Sensor_Type = sensor_type
                sensor.Sensor_Variant = sensor_variant
                sensor.Sensor_Name = sensor_name
                #sensor.Sensor_Metrics
                sensor.save()
                

        UNSPECIFIED_METRIC_COUNTER = 0
        #metrics       
        if dir.lower().startswith("metrics") and ("api_metric" in all_tables):
            f = open("../data/" + dir)
            textval = f.read()
            data = json.loads(textval)
            print(data)
            print("")
        
            for metric in data["data"]["items"]:
                metric_name = metric["name"]
                metric_id = metric["id"]

                metric_selected_id = 0
                metric_selected_name = ""
                metric_selected_precision = 0

                metric_unitdata = metric["units"]

                for unit in metric["units"]:
                    if 'selected' in unit:
                        metric_selected_id = unit['id']
                        metric_selected_name = unit['name']
                        metric_selected_precision = unit['precision']
                        print(unit)

                if not metric_selected_id: 
                    print("metric unit id from metric(id:" + str(metric_id) + ") from file " + str(dir) + " missing")
                    continue

                if (metric_selected_name == ""): 
                    UNSPECIFIED_METRIC_COUNTER += 1
                    print("metric '" + str(metric_id) + "' in file " + str(dir) + " has unspecified name. Setting to UNDEFINED_" + str(UNSPECIFIED_METRIC_COUNTER) + "!")
                    metric_selected_name = "UNDEFINED_" + str(UNSPECIFIED_METRIC_COUNTER)

                if (not metric_selected_precision): 
                    
                    print("metric '" + str(metric_id) + "' in file " + str(dir) + " has unspecified precision. Setting to 0!")
                
                qry = Metric.objects.filter(M_ID = metric_id)
                if qry.exists():
                    if printDebug: print("Metric " + str(metric_id) + " already exists in DB")
                    continue

                obj = Metric()
                obj.M_ID = metric_id
                obj.Name = metric_name
                obj.Selected_id = metric_selected_id
                obj.Selected_name = metric_selected_name
                obj.Selected_precision = metric_selected_precision
                obj.units = str(metric["units"]).replace("'",'"')

                obj.save()
                
                    # print(sensor_id + " " + sensor_type + " " + sensor_name)

                    # sensor = SensorType()
                    # sensor.Id = sensor_id
                    # sensor.Variant = sensor_type
                    # sensor.Name = sensor_name
                    # sensor.save()
                