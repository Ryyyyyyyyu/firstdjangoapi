# -*- coding: UTF-8 -*-
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from testsuites.models import TestsuitsModel


class TestsuitsModelSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(help_text='项目id', label='项目id', read_only=True, validators=[
        UniqueValidator(queryset=TestsuitsModel.objects.all(), message='测试用例id重复')])

    class Meta:
        model = TestsuitsModel
        exclude = ['is_delete']
        extra_kwargs = {
            'name': {
                'required': 'True',
                'error_messages': {
                    'max_length': '测试套件名称最大为50个字符',
                    'min_length': '测试套件名称不能为空',
                    'allow_null': '测试套件名称不能为null'
                },
                'validators': [UniqueValidator(queryset=TestsuitsModel.objects.all(), message='测试用例名称重复')]
            },
            'create_time': {'format': '%Y-%m-%d %H:%M:%S'},
            'update_time': {'format': '%Y-%m-%d %H:%M:%S'}
        }
