# -*- coding: UTF-8 -*-
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reports.models import ReportsModel


class ReportsModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReportsModel
        exclude = ['is_delete']
        read_only_fields = ['name', 'result', 'count', 'success']
        extra_kwargs = {
            'name': {
                'required': 'True',
                'error_messages': {
                    'max_length': '报告名称最大为200个字符',
                    'min_length': '报告名称不能为空',
                    'allow_null': '报告名称不能为null'
                },
                'validators': [UniqueValidator(queryset=ReportsModel.objects.all(), message='报告名称重复')]
            },
            'create_time': {'format': '%Y-%m-%d %H:%M:%S'},
            'update_time': {'format': '%Y-%m-%d %H:%M:%S'},
            'html': {'write_only': True},
            'summary': {'write_only': True},
        }
