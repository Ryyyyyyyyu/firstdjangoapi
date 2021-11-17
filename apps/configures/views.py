from django_filters import rest_framework
from rest_framework import viewsets, filters, permissions

from .models import ConfiguresModel
from .serializers import ConfiguresModelSerializer
from .filters import ConfigureFilterSet
# Create your views here.


class ConfigureViewSet(viewsets.ModelViewSet):
    queryset = ConfiguresModel.objects.all()
    serializer_class = ConfiguresModelSerializer

    # 过滤类和排序类
    filter_backends = [rest_framework.DjangoFilterBackend, filters.OrderingFilter]
    filter_class = ConfigureFilterSet

    search_fields = ['id', 'name']
    ordering_fields = ['id']

    permission_classes = [permissions.IsAuthenticated]
