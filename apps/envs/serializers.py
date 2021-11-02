# -*- coding: UTF-8 -*-
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from envs.models import EnvsModel


class EnvsModelSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(help_text='配置id', label='配置id', read_only=True, validators=[
        UniqueValidator(queryset=EnvsModel.objects.all(), message='配置id重复')])

    class Meta:
        model = EnvsModel
        exclude = ['is_delete']
        extra_kwargs = {
            'name': {
                'required': 'True',
                'error_messages': {
                    'max_length': '环境配置名称最大为50个字符',
                    'min_length': '环境配置名称不能为空',
                    'allow_null': '环境配置名称不能为null'
                },
                'validators': [UniqueValidator(queryset=EnvsModel.objects.all(), message='配置名称重复')]
            },
            'create_time': {'format': '%Y-%m-%d %H:%M:%S'},
            'update_time': {'format': '%Y-%m-%d %H:%M:%S'},
        }


class EnvsNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnvsModel
        fields = ['id', 'name']