# -*- coding: UTF-8 -*-
from django_filters import FilterSet, filters

from interfaces import models


class InterfacesFilterSet(FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = models.InterfacesModel
        fields = {
            'id': ['exact'],
        }
