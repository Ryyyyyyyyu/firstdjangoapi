# -*- coding: UTF-8 -*-
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import ProjectsModel
from interfaces.models import InterfacesModel


class ProjectSerializer(serializers.Serializer):
    id = serializers.IntegerField(help_text='项目id', label='项目id', required=False, validators=[
        UniqueValidator(queryset=ProjectsModel.objects.all(), message='项目id重复')])
    name = serializers.CharField(help_text='项目名称', label='项目名称', max_length=50, min_length=0, required=True,
                                 error_messages={
                                     'max_length': '项目名称最大为50个字符',
                                     'min_length': '项目名称不能为空',
                                     'allow_null': '项目名称不能为null'
                                 },
                                 validators=[UniqueValidator(queryset=ProjectsModel.objects.all(), message='项目名称重复')])
    leader = serializers.CharField(help_text='项目负责人', label='项目负责人', max_length=20,
                                   error_messages={
                                       'max_length': '项目负责人最大为20个字符'
                                   })
    desc = serializers.CharField(help_text='项目描述', label='项目描述', max_length=200, allow_null=True, allow_blank=True,
                                 required=False)
    create_time = serializers.DateTimeField(help_text='创建时间', label='创建时间', read_only=True, format='%Y-%m-%d %H:%M:%S')
    update_time = serializers.DateTimeField(help_text='更新时间', label='更新时间', read_only=True, format='%Y-%m-%d %H:%M:%S')
    # interfacesmodel_set = serializers.PrimaryKeyRelatedField(help_text='项目所属接口', label='项目所属接口', read_only=True,
    #                                                          many=True)



class InterfaceDataSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    tester = serializers.CharField()


class ProjectModelSerializer(serializers.ModelSerializer):
    interfacesmodel_set = InterfaceDataSerializer(read_only=True, many=True)

    # interfacesmodel_set = serializers.SerializerMethodField()

    # def get_interfacesmodel_set(self, obj):
    #     interfaces_query_set = obj.interfacesmodel_set.all()
    #     return [{'id': interface_obj.id, 'name': interface_obj.name} for interface_obj in interfaces_query_set]

    class Meta:
        model = ProjectsModel
        fields = "__all__"
        extra_kwargs = {
            'id': {
                'required': 'False',
                'validators': [UniqueValidator(queryset=ProjectsModel.objects.all(), message='项目id重复')]
            },
            'name': {
                'required': 'True',
                'error_messages': {
                    'max_length': '项目名称最大为50个字符',
                    'min_length': '项目名称不能为空',
                    'allow_null': '项目名称不能为null'
                },
                'validators': [UniqueValidator(queryset=ProjectsModel.objects.all(), message='项目名称重复')]
            }
        }
