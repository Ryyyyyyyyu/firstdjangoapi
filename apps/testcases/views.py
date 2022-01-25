import json

from django_filters import rest_framework
from rest_framework import filters
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import TestcasesFilterSet
from .serializers import TestcasesModelSerializer, TestcasesRunSerializer
from testcases.models import TestcasesModel
from utils import handler_datas
from utils.base_serializers import RunMixin


class TestcaseViewSet(RunMixin, viewsets.ModelViewSet):
    queryset = TestcasesModel.objects.all()
    serializer_class = TestcasesModelSerializer
    filter_backends = [rest_framework.DjangoFilterBackend, filters.OrderingFilter]
    filter_class = TestcasesFilterSet
    search_fields = ['id', 'name']
    ordering_fields = ['id']

    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        testcase_instance = self.get_object()
        try:
            testcase_include = json.loads(testcase_instance.include, encoding='utf-8')
        except Exception as e:
            return Response({"msg": f"include格式错误，{e}"})
        try:

            testcase_request = json.loads(testcase_instance.request, encoding='utf-8')
            # 获取request字段
            testcase_request_data = testcase_request.get('test').get('request')
            # request字段下json字段
            json_data = testcase_request_data.get('json')
            # 将json转化为str类型
            json_data_str = json.dumps(json_data, ensure_ascii=False)

            # 获取extract参数
            extract_data = testcase_request.get('test').get('extract')
            extract_data_list = handler_datas.handle_data3(extract_data)

            # 获取validate参数
            validate_data = testcase_request.get('test').get('validate')
            validate_data_list = handler_datas.handle_data1(validate_data)

            # 获取variables参数
            variables_data = testcase_request.get('test').get('variables')
            variables_data_list = handler_datas.handle_data2(variables_data)

            # 获取parameters参数
            parameters_data = testcase_request.get('test').get('parameters')
            parameters_data_list = handler_datas.handle_data3(parameters_data)

            # 获取setup_hooks参数
            setup_hooks_data = testcase_request.get('test').get('setup_hooks')
            setup_hooks_data_list = handler_datas.handle_data3(setup_hooks_data)

            # 获取teardown_hooks参数
            teardown_hooks_data = testcase_request.get('test').get('teardown_hooks')
            teardown_hooks_data_list = handler_datas.handle_data3(teardown_hooks_data)
            data = {
                "testcase_name": testcase_instance.name,
                "author": testcase_instance.author,
                "selected_configure_id": testcase_include.get('config'),
                "selected_interface_id": testcase_instance.interface_id,
                "selected_project_id": testcase_instance.interface.project_id,
                "selected_testcase_id": testcase_include.get('testcase', []),
                "method": testcase_request_data.get('method'),
                "url": testcase_request_data.get('url'),
                "param": handler_datas.handle_data4(testcase_request_data.get('param')),
                "header": handler_datas.handle_data4(testcase_request_data.get('headers')),
                "variable": handler_datas.handle_data2(testcase_request_data.get('data')),
                "jsonVariable": json_data_str,
                "extract": extract_data_list,
                "validate": validate_data_list,
                "globalVar": variables_data_list,
                "parameterized": parameters_data_list,
                "setupHooks": setup_hooks_data_list,
                "teardownHooks": teardown_hooks_data_list,
                "is_valid": testcase_instance.is_valid,
                "create_time": testcase_instance.create_time,
                "update_time": testcase_instance.update_time
            }
            return Response(data)
        except Exception as e:
            return Response({"msg": f"request格式错误，{e}"})

    @action(methods=['post'], detail=True)
    def run(self, request, *args, **kwargs):
        return self.execute(qs=[self.get_object()], request=request)

    def get_serializer_class(self):
        if self.action == 'run':
            serializer_class = TestcasesRunSerializer
        else:
            serializer_class = super().get_serializer_class()
        return serializer_class
