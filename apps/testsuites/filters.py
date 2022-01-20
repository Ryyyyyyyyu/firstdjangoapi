# -*- coding: UTF-8 -*-
from django_filters import FilterSet, filters

from testsuites import models


class TestsuitesFilterSet(FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = models.TestsuitsModel
        # fields = ['id', 'name']
        fields = {
            'id': ['exact'],
            # 'name': ['icontains']
        }
