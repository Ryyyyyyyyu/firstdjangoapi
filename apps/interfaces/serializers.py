# -*- coding: UTF-8 -*-
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from configures.serializers import ConfiguresNameSerializer
from interfaces.models import InterfacesModel
from projects.models import ProjectsModel
from testcases.serializers import TestcasesNameSerializer


class InterfacesModelSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(help_text='接口id', label='接口id', read_only=True, validators=[
        UniqueValidator(queryset=InterfacesModel.objects.all(), message='接口id重复')])
    # 重写project, 将PrimaryKeyRelatedField(help_text='接口所属项目', label='接口所属项目', queryset=ProjectsModel.objects.all())
    # 重写成StringRelatedField，序列化输出由id变成字段模型中的__str__方法的返回值
    project = serializers.StringRelatedField(label='所属项目名称', help_text='所属项目名称')
    project_id = serializers.PrimaryKeyRelatedField(label='所属项目id', help_text='所属项目id',
                                                    queryset=ProjectsModel.objects.all())

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

    def to_internal_value(self, data):
        result = super().to_internal_value(data)
        result['project'] = result.pop('project_id')
        return result


class InterfacesNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterfacesModel
        fields = ['id', 'name']


class InterfaceConfigureSerializer(serializers.ModelSerializer):
    configures = ConfiguresNameSerializer(help_text='接口配置信息', label='接口配置信息', read_only=True, many=True)

    class Meta:
        model = InterfacesModel
        fields = ['configures', ]


class InterfaceTestcaseSerializer(serializers.ModelSerializer):
    testcases = TestcasesNameSerializer(help_text='接口相关用例信息', label='接口相关用例信息', read_only=True, many=True)

    class Meta:
        model = InterfacesModel
        fields = ['testcases', ]
