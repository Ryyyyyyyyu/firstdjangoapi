from django_filters import rest_framework
from rest_framework import filters
from rest_framework import generics
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import permissions

from .filters import ProjectsFilterSet
from .models import ProjectsModel
from .serializers import ProjectModelSerializer


class ProjectsView(generics.ListCreateAPIView):
    queryset = ProjectsModel.objects.all()
    serializer_class = ProjectModelSerializer
    filter_backends = [rest_framework.DjangoFilterBackend, filters.OrderingFilter]
    filter_class = ProjectsFilterSet
    search_fields = ['id', 'name']
    ordering_fields = ['id']

    def put(self, request):
        try:
            objs = self.get_queryset().filter(id=request.data.get('id'))
        except Exception as e:
            return Response({"class": f"{self.__class__}", "method": "put", "msg": str(e)}, status=400)
        if objs.count() == 0:
            return Response({"class": f"{self.__class__}", "method": "put", "data": "项目id不存在"})
        serializer = self.get_serializer(instance=objs.first(), data=request.data)
        if not serializer.is_valid():
            return Response({"class": f"{self.__class__}", "method": "put", "msg": serializer.errors}, status=400)
        serializer.save()

        return Response({"class": f"{self.__class__}", "method": "put", "data": "更新项目成功"})

    def delete(self, request):
        self.get_queryset().delete()
        return Response({"class": f"{self.__class__}", "method": "delete", "data": "删除所有项目成功"})


class ProjectDetailsViews(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProjectsModel.objects.all()
    serializer_class = ProjectModelSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        data['id'] = kwargs['pk']
        serializer = self.serializer_class(data=data)
        if not serializer.is_valid():
            return Response({"class": f"{self.__class__}", "method": "post", "msg": serializer.errors}, status=400)
        serializer.save()
        return Response({"class": f"{self.__class__}", "method": "post", "data": "创建项目成功"}, status=201)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = ProjectsModel.objects.all()
    serializer_class = ProjectModelSerializer
    filter_backends = [rest_framework.DjangoFilterBackend, filters.OrderingFilter]
    filter_class = ProjectsFilterSet
    search_fields = ['id', 'name']
    ordering_fields = ['id']

    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False)
    def names(self, request, *args, **kwargs):
        instance = self.get_queryset()

        return Response([{'id': project.id, 'name': project.name} for project in instance])

    @action(methods=['get'], detail=True)
    def interfaces(self, request, *args, **kwargs):
        project = self.get_object()
        interfaces_qs = project.interfacesmodel_set.all()
        interfaces_data = [{'id': interface.id, 'name': interface.name} for interface in interfaces_qs]
        return Response(interfaces_data, status=200)
