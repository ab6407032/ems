from django.urls import path
from rest_framework import routers

from . import views

router_auth = routers.DefaultRouter()
router_auth.register('auth', views.AuthenticateViewset)
