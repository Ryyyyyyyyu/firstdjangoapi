# -*- coding: UTF-8 -*-
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from interfaces.models import InterfacesModel
from projects.models import ProjectsModel
from configures.models import ConfiguresModel


def is_exit_project_id(value):
    if not ProjectsModel.objects.filter(id=value).exists():
        raise serializers.ValidationError('项目id不存在')


class InterfaceProjectSerializer(serializers.ModelSerializer):
    """
    获取接口所属项目信息
    """
    project = serializers.StringRelatedField(label='所属项目名称', help_text='所属项目名称', read_only=True)
    pid = serializers.IntegerField(label='所属项目id', help_text='所属项目id', write_only=True,
                                   validators=[is_exit_project_id])
    iid = serializers.IntegerField(label='所属接口id', help_text='所属接口id', write_only=True)

    class Meta:
        model = InterfacesModel
        fields = ['name', 'project', 'iid', 'pid']
        extra_kwargs = {
            'name': {
                'read_only': True
            }
        }

    # 校验项目传入的项目id和接口id是否匹配
    def validate(self, attrs):
        if not InterfacesModel.objects.filter(id=attrs.get('iid'), project_id=attrs.get('pid')):
            raise serializers.ValidationError('项目和接口不对应')
        return attrs


class ConfiguresModelSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(help_text='配置id', label='配置id', read_only=True, validators=[
        UniqueValidator(queryset=InterfacesModel.objects.all(), message='配置id重复')])
    interface = InterfaceProjectSerializer(help_text='配置所属接口以及项目', label='配置所属接口以及项目')

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

    # 将输入的iid和pid替换成interface_id
    def to_internal_value(self, data):
        result = super().to_internal_value(data)
        iid = result.get('interface').get('iid')
        result.pop('interface')
        result['interface_id'] = iid
        return result
