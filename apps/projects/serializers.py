# -*- coding: UTF-8 -*-
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from projects.models import ProjectsModel
from debugtalks.models import DebugtalksModel
from interfaces.serializers import InterfacesNameSerializer


class ProjectModelSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(help_text='项目id', label='项目id', read_only=True, validators=[
        UniqueValidator(queryset=ProjectsModel.objects.all(), message='项目id重复')])

    class Meta:
        model = ProjectsModel
        # fields = "__all__"
        exclude = ['is_delete']
        extra_kwargs = {
            'name': {
                'required': 'True',
                'error_messages': {
                    'max_length': '项目名称最大为50个字符',
                    'min_length': '项目名称不能为空',
                    'allow_null': '项目名称不能为null'
                },
                'validators': [UniqueValidator(queryset=ProjectsModel.objects.all(), message='项目名称重复')]
            },
            'create_time': {'format': '%Y-%m-%d %H:%M:%S'},
            'update_time': {'format': '%Y-%m-%d %H:%M:%S'}
        }

    def create(self, validated_data):
        instance = super().create(validated_data)
        DebugtalksModel.objects.create(project=instance)
        return instance


class ProjectNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectsModel
        fields = ['id', 'name']


class ProjectInterfaceSerializer(serializers.ModelSerializer):
    interfaces = InterfacesNameSerializer(help_text='项目接口信息', label='项目接口信息', read_only=True, many=True)

    class Meta:
        model = ProjectsModel
        fields = ['interfaces']
