# -*- coding: UTF-8 -*-
from rest_framework import routers

from debugtalks import views


router = routers.DefaultRouter()
router.register('', views.DebugtalkViewSet)

urlpatterns = []
urlpatterns += router.urls


