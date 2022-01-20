# -*- coding: UTF-8 -*-
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from testcases.models import TestcasesModel
from configures.serializers import InterfaceProjectSerializer


class TestcasesModelSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(help_text='项目id', label='项目id', read_only=True, validators=[
        UniqueValidator(queryset=TestcasesModel.objects.all(), message='测试用例id重复')])
    interface = InterfaceProjectSerializer(label='所属项目和接口信息', help_text='所属项目和接口信息')

    class Meta:
        model = TestcasesModel
        exclude = ['is_delete']
        extra_kwargs = {
            'name': {
                'required': 'True',
                'error_messages': {
                    'max_length': '测试用例名称最大为50个字符',
                    'min_length': '测试用例名称不能为空',
                    'allow_null': '测试用例名称不能为null'
                },
                'validators': [UniqueValidator(queryset=TestcasesModel.objects.all(), message='测试用例名称重复')]
            },
            'create_time': {'format': '%Y-%m-%d %H:%M:%S'},
            'update_time': {'format': '%Y-%m-%d %H:%M:%S'}
        }

    # 将输入的iid和pid替换成interface_id
    def to_internal_value(self, data):
        result = super().to_internal_value(data)
        iid = result.get('interface').get('iid')
        result.pop('interface')
        result['interface_id'] = iid
        return result


class TestcasesNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestcasesModel
        fields = ['id', 'name']


class TestcasesRunSerializer(serializers.ModelSerializer):
    evn_id = serializers.IntegerField(help_text='所属环境id', label='所属环境id',
                                      validators=[])

    class Meta:
        model = TestcasesModel
        fields = ['id', 'evn_id']
