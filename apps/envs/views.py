from rest_framework import viewsets, permissions
from rest_framework import filters
from django_filters import rest_framework
from rest_framework.decorators import action

from envs.models import EnvsModel
from envs.serializers import EnvsModelSerializer
from envs.serializers import EnvsNameSerializer
from envs.filters import EnvsFilterSet
# Create your views here.


class EnvViewSet(viewsets.ModelViewSet):
    queryset = EnvsModel.objects.all()
    serializer_class = EnvsModelSerializer

    filter_backends = [rest_framework.DjangoFilterBackend, filters.OrderingFilter]
    filter_class = EnvsFilterSet

    search_fields = ['id', 'name']
    ordering_fields = ['id']

    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False)
    def names(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset().exclude(is_delete=True)
        return queryset

    def get_serializer_class(self):
        if self.action == 'names':
            return EnvsNameSerializer
        else:
            serializer_class = super().get_serializer_class()
            return serializer_class

    def paginate_queryset(self, queryset):
        if self.action == 'names':
            return None
        else:
            return super().paginate_queryset(queryset)
