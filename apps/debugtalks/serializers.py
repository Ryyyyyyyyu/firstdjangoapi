# -*- coding: UTF-8 -*-
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from debugtalks.models import DebugtalksModel


class DebugtalksModelSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(help_text='debugtalk_id', label='debugtalk_id', read_only=True, validators=[
        UniqueValidator(queryset=DebugtalksModel.objects.all(), message='debugtalk_id重复')])
    project = serializers.StringRelatedField(label='所属项目名称', help_text='所属项目名称', read_only=True)
    # project = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = DebugtalksModel
        # fields = ['id', 'debugtalk', 'is_valid', 'create_time', 'update_time']
        exclude = ['is_delete']
        extra_kwargs = {
            'debugtalk': {'write_only': True},
            'create_time': {'format': '%Y-%m-%d %H:%M:%S'},
            'update_time': {'format': '%Y-%m-%d %H:%M:%S'},
        }


class DebugtalksContextSerializer(serializers.ModelSerializer):
    class Meta:
        model = DebugtalksModel
        fields = ['id', 'debugtalk']
