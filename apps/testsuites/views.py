import json

from django_filters import rest_framework
from rest_framework import filters
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import TestsuitesFilterSet
from .serializers import TestsuitsModelSerializer
from .models import TestsuitsModel
from utils import handler_datas


class TestcaseViewSet(viewsets.ModelViewSet):
    queryset = TestsuitsModel.objects.all()
    serializer_class = TestsuitsModelSerializer
    filter_backends = [rest_framework.DjangoFilterBackend, filters.OrderingFilter]
    filter_class = TestsuitesFilterSet
    search_fields = ['id', 'name']
    ordering_fields = ['id']

    permission_classes = [permissions.IsAuthenticated]
