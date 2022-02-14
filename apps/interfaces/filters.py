# -*- coding: UTF-8 -*-
from django_filters import FilterSet, filters

from interfaces import models


class InterfacesFilterSet(FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    project_id = filters.CharFilter(field_name='project', lookup_expr='exact')

    class Meta:
        model = models.InterfacesModel
        fields = {
            'id': ['exact'],
        }
