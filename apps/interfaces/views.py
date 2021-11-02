from django.views import View
from django.http import JsonResponse
from rest_framework import viewsets, permissions
from rest_framework import filters
from django_filters import rest_framework

# Create your views here.
from rest_framework.decorators import action

from configures.models import ConfiguresModel
from interfaces.filters import InterfacesFilterSet
from interfaces.models import InterfacesModel
from interfaces.serializers import InterfacesModelSerializer, InterfacesNameSerializer, InterfaceConfigureSerializer, \
    InterfaceTestcaseSerializer
from testcases.models import TestcasesModel


class InterfaceViewSet(viewsets.ModelViewSet):
    queryset = InterfacesModel.objects.all()
    serializer_class = InterfacesModelSerializer

    # 过滤类和排序类
    filter_backends = [rest_framework.DjangoFilterBackend, filters.OrderingFilter]
    filter_class = InterfacesFilterSet

    search_fields = ['id', 'name']
    ordering_fields = ['id']

    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False)
    def names(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(methods=['get'], detail=True)
    def configure(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        response.data = response.data.get('configures')
        return response

    @action(methods=['get'], detail=True)
    def testcases(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        response.data = response.data.get('testcases')
        return response

    def get_queryset(self):
        queryset = super().get_queryset().exclude(is_delete=True)
        return queryset

    def get_serializer_class(self):
        if self.action == 'names':
            return InterfacesNameSerializer
        elif self.action == 'configure':
            return InterfaceConfigureSerializer
        elif self.action == 'testcases':
            return InterfaceTestcaseSerializer
        else:
            serializer_class = super().get_serializer_class()
            return serializer_class

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        for item in response.data.get('results'):
            item['testcases'] = TestcasesModel.objects.filter(interface_id=item.get('id')).count()
            item['configures'] = ConfiguresModel.objects.filter(interface_id=item.get('id')).count()
        return response

