from django.shortcuts import render, HttpResponse
from .models import MetricEntry, SensorType, Metric, SensorData


# Create your views here.
def index(request):
    return HttpResponse("test")

def apiGetMetricData(request):
    retvals = []

    opts = dict(request.GET.items())
    if opts:
        #print(opts)
        if "m_id" in opts:
            #specific metric_id related readings
            metrics = MetricEntry.objects.filter(M_ID=opts["m_id"]).values()
            for i in metrics:
                retvals.append(i)
        
        elif "sensor_id" in opts:
            #specific sensor_id
            metrics = MetricEntry.objects.filter(Sensor_ID=opts["sensor_id"])
            for i in metrics:
                retvals.append(i)
    else:
        metrics = MetricEntry.objects.all().values()
        for i in metrics:
            retvals.append(i)

    #print(str(retvals))

    return HttpResponse(str(retvals).replace("'",'"'))


def apiGetSensorMake(request):
    retval = []
    opts = dict(request.GET.items())
    #print(opts)

    if "sensor_type" in opts:
        if "sensor_variant" in opts:
            s_type = int(opts["sensor_type"])
            s_variant = int(opts["sensor_variant"])
            sensor = SensorType.objects.filter(S_Id=s_type, S_Variant=s_variant).values()
            for i in sensor:
                retval.append(i["S_Name"])

            if (retval == []):
                retval.append("undefined")

    else:
        sensor = SensorType.objects.all().values()
        for i in sensor:
            retval.append(i)
    
    #print(retval)

    return HttpResponse(str(retval).replace("'",'"'))

def apiGetSensorData(request):
    retval = []
    opts = dict(request.GET.items())
    #print(opts)
    if "sensor_id" in opts:
        qry = SensorData.objects.filter(Sensor_ID=opts["sensor_id"]).values()
        for i in qry:
            #print(i)
            retval.append(i)
        
    return HttpResponse(retval)


def apiGetMetrics(request):
    retval = []
    opts = dict(request.GET.items())
    #print(opts)
    if "type" in opts:
        if opts["type"] == "all":
            metrics = Metric.objects.all().values()
            if metrics.exists():
                for m in metrics:
                    m.pop("units")
                    retval.append(m)

        elif opts["type"] == "metric_ids":
            metrics = Metric.objects.all().values()
            if metrics.exists():
                for m in metrics:
                    retval.append(m["M_ID"])

    metrics = Metric.objects.all().values()
    
    encoded = str(retval).replace("'",'"').replace(' "[',' [').replace(']",','],')

    return HttpResponse(encoded)



