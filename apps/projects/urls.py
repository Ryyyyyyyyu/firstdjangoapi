# -*- coding: UTF-8 -*-
from django.urls import path, re_path, include
from rest_framework import routers

from apps.projects import views


rt = routers.DefaultRouter()
rt.register('project', views.ProjectViewSet)

urlpatterns = [
    # path('articles/<dater:pk>/', views.test),
    # re_path(r'^projects/(?P<pk>\w{3})/$', views.test1),

    # path('projectsdetail/', views.ProjectsView.as_view()),
    # path('projectsdetail/<int:pk>/', views.ProjectDetailsViews.as_view()),
    # path('projectset/', views.ProjectViewSet.as_view({
    #     'get': 'list',
    #     'post': 'create'
    # })),
    # path('projectset/<int:pk>/', views.ProjectViewSet.as_view({
    #     'get': 'retrieve',
    #     'put': 'update',
    #     'patch': 'partial_update',
    #     'delete': 'destroy'
    # })),
    # path('names/', views.ProjectViewSet.as_view({
    #     'get': 'names'
    # })),
    # path('<int:pk>/interfaces/', views.ProjectViewSet.as_view({
    #     'get': 'interfaces'
    # })),
    # path('', include(rt.urls)),
]
urlpatterns += rt.urls
