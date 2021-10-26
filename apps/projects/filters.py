# -*- coding: UTF-8 -*-
from django_filters import FilterSet, filters

from apps.projects import models


class ProjectsFilterSet(FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = models.ProjectsModel
        # fields = ['id', 'name']
        fields = {
            'id': ['exact'],
            # 'name': ['icontains']
        }
