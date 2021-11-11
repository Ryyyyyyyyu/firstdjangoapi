from rest_framework import viewsets, permissions, mixins
from rest_framework import filters
from rest_framework.decorators import action
from django_filters import rest_framework

from debugtalks.models import DebugtalksModel
from debugtalks.serializers import DebugtalksModelSerializer
from debugtalks.serializers import DebugtalksContextSerializer
from debugtalks.filters import DebugtalkFilterSet


class DebugtalkViewSet(mixins.UpdateModelMixin, viewsets.ReadOnlyModelViewSet):
    queryset = DebugtalksModel.objects.all()
    serializer_class = DebugtalksModelSerializer

    # 过滤类和排序类
    filter_backends = [rest_framework.DjangoFilterBackend, filters.OrderingFilter]
    filter_class = DebugtalkFilterSet

    search_fields = ['id', 'name']
    ordering_fields = ['id']

    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DebugtalksContextSerializer
        else:
            return super().get_serializer_class()
