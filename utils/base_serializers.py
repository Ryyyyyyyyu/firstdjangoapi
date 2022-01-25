import os
from collections import Iterable
from datetime import datetime

from django.db.models.query import QuerySet
from rest_framework.response import Response

from envs.models import EnvsModel
from firstdjangoapi import settings
from utils import common


class RunMixin:

    def execute(self, qs, request):
        # 1.获取用例模型对象以及evn_id
        if not isinstance(qs, Iterable):
            return Response({'msg': '测试用例数据不可迭代，请检查qs数据，用例执行失败'})
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        env_id = serializer.validated_data.get('evn_id')
        env = EnvsModel.objects.filter(id=env_id).first()

        # 2.创建以时间戳命明的目录
        dirname = datetime.strftime(datetime.now(), '%Y%m%d%H%M%S')
        testcase_dir_path = os.path.join(settings.PROJECT_DIR, dirname)
        os.makedirs(testcase_dir_path)

        # 3.创建以项目名命名的目录
        # 4.生成debug.py、yaml用例文件
        for instance in qs:
            common.generate_testcase_file(instance, env, testcase_dir_path)

        # 5.运行用例并生成测试报告
        return common.run_testcase(instance, testcase_dir_path)
