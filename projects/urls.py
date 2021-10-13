# -*- coding: UTF-8 -*-
from django.urls import path, re_path
from . import views


urlpatterns = [
    # path('articles/<dater:pk>/', views.test),
    # re_path(r'^projects/(?P<pk>\w{3})/$', views.test1),

    path('projectsdetail/', views.ProjectsView.as_view()),
    path('projectsdetail/<int:pk>/', views.ProjectDetailsViews.as_view()),
    path('projectset/', views.ProjectViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('projectset/<int:pk>/', views.ProjectViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
]
