# -*- coding: UTF-8 -*-
from rest_framework import serializers

from testcases.models import TestcasesModel


class TestcasesNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestcasesModel
        fields = ['id', 'name']
