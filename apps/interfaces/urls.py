# -*- coding: UTF-8 -*-
from django.urls import path, re_path
from interfaces import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register('', views.InterfaceViewSet)

urlpatterns = [
]
urlpatterns += router.urls
