# -*- coding: UTF-8 -*-
from django.urls import path, re_path, include
from rest_framework import routers

from projects import views


router = routers.DefaultRouter()
router.register('', views.ProjectViewSet)

urlpatterns = [
]
urlpatterns += router.urls
