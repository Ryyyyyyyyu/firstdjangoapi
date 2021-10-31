# -*- coding: UTF-8 -*-
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from interfaces.models import InterfacesModel


class InterfacesModelSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(help_text='接口id', label='接口id', read_only=True, validators=[
        UniqueValidator(queryset=InterfacesModel.objects.all(), message='接口id重复')])

    class Meta:
        model = InterfacesModel
        exclude = ['is_delete']
        extra_kwargs = {
            'name': {
                'required': 'True',
                'error_messages': {
                    'max_length': '接口名称最大为50个字符',
                    'min_length': '接口名称不能为空',
                    'allow_null': '接口名称不能为null'
                },
                'validators': [UniqueValidator(queryset=InterfacesModel.objects.all(), message='接口名称重复')]
            },
            'create_time': {'format': '%Y-%m-%d %H:%M:%S'},
            'update_time': {'format': '%Y-%m-%d %H:%M:%S'},
        }


class InterfacesNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = InterfacesModel
        fields = ['id', 'name']
