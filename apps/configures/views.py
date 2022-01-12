import json

from django_filters import rest_framework
from rest_framework import viewsets, filters, permissions
from rest_framework.response import Response

from .models import ConfiguresModel
from .serializers import ConfiguresModelSerializer
from .filters import ConfigureFilterSet
from utils import handler_datas
# Create your views here.


class ConfigureViewSet(viewsets.ModelViewSet):
    queryset = ConfiguresModel.objects.all()
    serializer_class = ConfiguresModelSerializer

    # 过滤类和排序类
    filter_backends = [rest_framework.DjangoFilterBackend, filters.OrderingFilter]
    filter_class = ConfigureFilterSet

    search_fields = ['id', 'name', 'is_valid']
    ordering_fields = ['id']

    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        config_instance = self.get_object()
        config_request = json.loads(config_instance.request, encoding='utf-8')

        # 处理请求头
        config_headers = config_request.get('config').get('request').get('headers')
        config_headers_list = handler_datas.handle_data4(config_headers)

        # 处理全局变量数据
        config_variables = config_request.get('config').get('variables')
        config_variables_list = handler_datas.handle_data2(config_variables)

        config_name = config_request.get('config').get('name')
        select_interface_id = config_instance.interface_id
        select_project_id = config_instance.interface.project_id

        data = {
            "config_name": config_name,
            "author": config_instance.author,
            "header": config_headers_list,
            "globalVar": config_variables_list,
            "select_interface_id": select_interface_id,
            "select_project_id": select_project_id,
            "is_valid": config_instance.is_valid,
            "create_time": config_instance.create_time,
            "update_time": config_instance.update_time
        }
        return Response(data)
