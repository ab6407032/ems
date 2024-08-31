from django.urls import path
from rest_framework import routers
from frontend.urls import router_frontend
from . import views

router_notification = routers.DefaultRouter()

router_notification.register('notification', views.TemplateViewset)
router_notification.register('otp', views.OTPViewset)

router_frontend.register('otp', views.OTPViewset)