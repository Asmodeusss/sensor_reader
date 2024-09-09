from django.urls import path

from . import views

app_name = "api"
urlpatterns = [

    # /polls/index
    path("", views.index, name="index"),
    path("getMetricData/", views.apiGetMetricData, name="getMetricData"),
    path("getSensorMake/", views.apiGetSensorMake, name="getSensorMake"),
    path("getMetrics/", views.apiGetMetrics, name="getMetrics"),
    path("getSensor/", views.apiGetSensorData, name="getSensor")

]