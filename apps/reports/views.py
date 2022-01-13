import json

from django.http import StreamingHttpResponse
from rest_framework import permissions, mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action

from reports.models import ReportsModel
from reports.serializers import ReportsModelSerializer


class ReportViewSet(mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):
    queryset = ReportsModel.objects.all()
    serializer_class = ReportsModelSerializer

    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            summary = json.loads(instance.summary, encoding='utf-8')
            return Response({
                'id': instance.id,
                'summary': summary
            })
        except Exception as e:
            return Response({"msg": f"summary格式错误，{e}"})

    def file_iterator(self, file_name, chunk_size=512):
        with open(file_name) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    @action(detail=True)
    def download(self, request, *args, **kwargs):
        # TODO
        # 中文乱码问题待修复
        # 获取模型对象数据（数据库数据）
        instance = self.get_object()
        # 获取测试报告页面源码
        byte_data = instance.html
        response = StreamingHttpResponse(iter(byte_data))
        # 添加响应头参数
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = f'attachment;filename*=UTF-8"{instance.name}.html"'
        return response
