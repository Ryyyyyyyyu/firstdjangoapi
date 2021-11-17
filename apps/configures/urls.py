# -*- coding: UTF-8 -*-
from rest_framework import routers

from configures import views


router = routers.DefaultRouter()
router.register('', views.ConfigureViewSet)

urlpatterns = []
urlpatterns += router.urls


