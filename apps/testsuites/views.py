import json

from django_filters import rest_framework
from rest_framework import filters
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import TestsuitesFilterSet
from .serializers import TestsuitsModelSerializer, TestsuitsRunSerializer
from .models import TestsuitsModel
from testcases.models import TestcasesModel
from utils.base_serializers import RunMixin


class TestcaseViewSet(RunMixin, viewsets.ModelViewSet):
    queryset = TestsuitsModel.objects.all()
    serializer_class = TestsuitsModelSerializer
    filter_backends = [rest_framework.DjangoFilterBackend, filters.OrderingFilter]
    filter_class = TestsuitesFilterSet
    search_fields = ['id', 'name']
    ordering_fields = ['id']

    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['post'], detail=True)
    def run(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            include = json.loads(instance.include)
        except Exception as e:
            return Response({'msg': f'include数据格式异常，{e}'})
        testcases_list = []
        for interface_id in include:
            testcases_qs = TestcasesModel.objects.filter(interface_id=interface_id)
            testcases_list.extend(testcases_qs)
        return self.execute(qs=testcases_list, request=request)

    def get_serializer_class(self):
        if self.action == 'run':
            serializer_class = TestsuitsRunSerializer
        else:
            serializer_class = super().get_serializer_class()
        return serializer_class

