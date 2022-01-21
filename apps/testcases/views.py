import json
import os
from datetime import datetime

from django_filters import rest_framework
from rest_framework import filters
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from firstdjangoapi import settings
from .filters import TestcasesFilterSet
from .serializers import TestcasesModelSerializer, TestcasesRunSerializer
from testcases.models import TestcasesModel
from envs.models import EnvsModel
from utils import handler_datas
from utils import common


class TestcaseViewSet(viewsets.ModelViewSet):
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
        # 1.获取用例模型对象以及evn_id
        instance = self.get_object()
        serializer: TestcasesRunSerializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(True)
        env_id = serializer.validated_data.get('evn_id')
        env = EnvsModel.objects.filter(id=env_id).first()

        # 2.创建以时间戳命明的目录
        dirname = datetime.strftime(datetime.now(), '%Y%m%d%H%M%S')
        testcase_dir_path = os.path.join(settings.PROJECT_DIR, dirname)
        os.makedirs(testcase_dir_path)

        # 3.创建以项目名命名的目录
        # 4.生成debug.py、yaml用例文件
        common.generate_testcase_file(instance, env, testcase_dir_path)

        # 5.运行用例并生成测试报告
        return common.run_testcase(instance, testcase_dir_path)

    def get_serializer_class(self):
        if self.action == 'run':
            serializer_class = TestcasesRunSerializer
        else:
            serializer_class = super().get_serializer_class()
        return serializer_class
