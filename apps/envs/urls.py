# -*- coding: UTF-8 -*-
from rest_framework import routers

from envs import views


router = routers.DefaultRouter()
router.register('', views.EnvViewSet)


