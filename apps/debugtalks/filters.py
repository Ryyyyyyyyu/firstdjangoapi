# -*- coding: UTF-8 -*-
from django_filters import FilterSet, filters

from debugtalks import models


class DebugtalkFilterSet(FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = models.DebugtalksModel
        fields = {
            'id': ['exact'],
        }
