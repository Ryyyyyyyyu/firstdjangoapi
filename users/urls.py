# -*- coding: UTF-8 -*-
from django.urls import path, re_path
from rest_framework_jwt.views import obtain_jwt_token
from . import views

urlpatterns = [
    path('login/', obtain_jwt_token),
    path('register/', views.UserView.as_view()),
    re_path(r'^(?P<username>\w{4,20})/count/$', views.UserExistCountView.as_view()),
    re_path(r'^(?P<email>[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+)/count/$',
            views.EmailExistCountView.as_view()),
]


