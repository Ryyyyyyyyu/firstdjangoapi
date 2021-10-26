# -*- coding: UTF-8 -*-
from django.urls import path, re_path
from interfaces import views


urlpatterns = [
    # path('articles/<dater:pk>/', views.test),
    # re_path(r'^projects/(?P<pk>\w{3})/$', views.test1),

    path('interfaces/', views.InterfacesView.as_view()),
]
