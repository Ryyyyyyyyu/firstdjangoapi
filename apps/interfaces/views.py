from django.views import View
from django.http import JsonResponse
from rest_framework import viewsets, permissions
from rest_framework import filters
from django_filters import rest_framework

# Create your views here.
from interfaces.filters import InterfacesFilterSet
from interfaces.models import InterfacesModel
from interfaces.serializers import InterfacesModelSerializer


class InterfaceViewSet(viewsets.ModelViewSet):
    queryset = InterfacesModel.objects.all()
    serializer_class = InterfacesModelSerializer

    # 过滤类和排序类
    filter_backends = [rest_framework.DjangoFilterBackend, filters.OrderingFilter]
    filter_class = InterfacesFilterSet

    search_fields = ['id', 'name']
    ordering_fields = ['id']

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset().exclude(is_delete=True)
        return queryset
