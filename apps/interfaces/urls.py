# -*- coding: UTF-8 -*-
from django.urls import path, re_path
from rest_framework import routers

from interfaces import views

router = routers.DefaultRouter()
router.register('', views.InterfaceViewSet)

urlpatterns = [
]
urlpatterns += router.urls
