from django_filters import rest_framework
from rest_framework import filters
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from configures.models import ConfiguresModel
from interfaces.models import InterfacesModel
from projects.filters import ProjectsFilterSet
from projects.models import ProjectsModel
from projects.serializers import ProjectModelSerializer, ProjectNameSerializer, ProjectInterfaceSerializer
from projects.serializers import ProjectsRunSerializer
from testcases.models import TestcasesModel
from testsuites.models import TestsuitsModel
from utils.base_serializers import RunMixin


class ProjectViewSet(RunMixin, viewsets.ModelViewSet):
    """
    list:
    获取所有项目列表数据，默认分页

    create:
    创建项目

    read:
    获取具体某个项目信息

    update:
    更新某个项目信息（全部）

    partial_update:
    更新某个项目信息（部分）

    delete:
    删除项目

    name:
    获取所有项目id和名称，不分页

    interfaces:
    获取项目包含的接口名称和id
    """
    queryset = ProjectsModel.objects.all()
    serializer_class = ProjectModelSerializer
    filter_backends = [rest_framework.DjangoFilterBackend, filters.OrderingFilter]
    filter_class = ProjectsFilterSet
    search_fields = ['id', 'name']
    ordering_fields = ['id']

    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False)
    def names(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(methods=['get'], detail=True)
    def interfaces(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        response.data = response.data.get('interfaces')
        return response

    @action(methods=['post'], detail=True)
    def run(self, request, *args, **kwargs):
        testcase_qs = TestcasesModel.objects.filter(interface__project=self.get_object())
        if len(testcase_qs) == 0:
            return Response({'msg': '此项目下没有用例，无法执行！'})
        return self.execute(qs=testcase_qs, request=request)

    def get_queryset(self):
        queryset = super().get_queryset().exclude(is_delete=True)
        return queryset

    def get_serializer_class(self):
        if self.action == 'names':
            return ProjectNameSerializer
        elif self.action == 'interfaces':
            return ProjectInterfaceSerializer
        elif self.action == 'run':
            return ProjectsRunSerializer
        else:
            serializer_class = super().get_serializer_class()
            return serializer_class

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        for item in response.data.get('results'):
            item['interfaces'] = InterfacesModel.objects.filter(project_id=item.get('id')).count()
            item['testsuits'] = TestsuitsModel.objects.filter(project_id=item.get('id')).count()
            item['testcases'] = TestcasesModel.objects.filter(interface__project__id=item.get('id')).count()
            item['configures'] = ConfiguresModel.objects.filter(interface__project__id=item.get('id')).count()
        return response

    def paginate_queryset(self, queryset):
        if self.action == 'names':
            return None
        else:
            return super().paginate_queryset(queryset)

