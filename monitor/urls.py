
from django.urls import path
# from django.conf.urls import include,url
from .views import *
from rest_framework import routers

router_monitor = routers.DefaultRouter()
router_monitor.register('monitor/node', NodeMonitorViewset)