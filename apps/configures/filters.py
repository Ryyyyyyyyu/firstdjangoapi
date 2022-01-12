# -*- coding: UTF-8 -*-
from django_filters import FilterSet, filters

from configures import models


class ConfigureFilterSet(FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    is_valid = filters.BooleanFilter(field_name='is_valid')

    class Meta:
        model = models.ConfiguresModel
        fields = {
            'id': ['exact'],
        }
