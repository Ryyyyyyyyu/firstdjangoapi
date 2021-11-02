# -*- coding: UTF-8 -*-
from django_filters import FilterSet, filters

from envs import models


class EnvsFilterSet(FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = models.EnvsModel
        fields = {
            'id': ['exact'],
        }
