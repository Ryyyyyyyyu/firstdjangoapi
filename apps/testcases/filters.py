# -*- coding: UTF-8 -*-
from django_filters import FilterSet, filters

from testcases import models


class TestcasesFilterSet(FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = models.TestcasesModel
        # fields = ['id', 'name']
        fields = {
            'id': ['exact'],
            # 'name': ['icontains']
        }
