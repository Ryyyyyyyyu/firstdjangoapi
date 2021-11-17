# -*- coding: UTF-8 -*-
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from interfaces.models import InterfacesModel
from configures.models import ConfiguresModel


class ConfiguresModelSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(help_text='配置id', label='配置id', read_only=True, validators=[
        UniqueValidator(queryset=InterfacesModel.objects.all(), message='配置id重复')])

    class Meta:
        model = ConfiguresModel
        exclude = ['is_delete']
        extra_kwargs = {
            'name': {
                'required': 'True',
                'error_messages': {
                    'max_length': '配置名称最大为50个字符',
                    'min_length': '配置名称不能为空',
                    'allow_null': '配置名称不能为null'
                },
                'validators': [UniqueValidator(queryset=ConfiguresModel.objects.all(), message='配置名称重复')]
            },
            'request': {'write_only': True},
            'create_time': {'format': '%Y-%m-%d %H:%M:%S'},
            'update_time': {'format': '%Y-%m-%d %H:%M:%S'},
        }


class ConfiguresNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfiguresModel
        fields = ['id', 'name']
