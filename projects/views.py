import json

from django.http import JsonResponse
from rest_framework.response import Response
from django.views import View
from rest_framework.views import APIView
from rest_framework import filters
from django_filters import rest_framework
from rest_framework.generics import GenericAPIView

from .models import ProjectsModel
from .filters import ProjectsFilterSet
from .serializers import ProjectModelSerializer


# Create your views here.
# class ProjectsView(View):
# class ProjectsView(APIView):
class ProjectsView(GenericAPIView):
    queryset = ProjectsModel.objects.all()
    serializer_class = ProjectModelSerializer
    filter_backends = [rest_framework.DjangoFilterBackend, filters.OrderingFilter]
    filter_class = ProjectsFilterSet
    search_fields = ['id', 'name']
    ordering_fields = ['id']

    def get(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(instance=page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(instance=queryset, many=True)
        return Response({"class": f"{self.__class__}", "method": "get", "data": serializer.data})

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"class": f"{self.__class__}", "method": "post", "msg": serializer.errors})
        serializer.save()
        return Response({"class": f"{self.__class__}", "method": "post", "data": "创建项目成功"}, status=201)

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


class ProjectDetailsViews(GenericAPIView):
    queryset = ProjectsModel.objects.all()
    serializer_class = ProjectModelSerializer

    def get(self, request, *args, **kwargs):
        objs = self.get_object()
        serializer = self.serializer_class(instance=objs)
        return Response({"class": f"{self.__class__}", "method": "get", "data": serializer.data})

    def post(self, request, *args, **kwargs):
        data = request.data
        data['id'] = kwargs['pk']
        serializer = self.serializer_class(data=data)
        if not serializer.is_valid():
            return Response({"class": f"{self.__class__}", "method": "post", "msg": serializer.errors}, status=400)
        serializer.save()
        return Response({"class": f"{self.__class__}", "method": "post", "data": "创建项目成功"}, status=201)

    def put(self, request, *args, **kwargs):
        try:
            objs = self.get_object()
        except Exception as e:
            return Response({"msg": str(e)})

        serializer = self.get_serializer(instance=objs, data=request.data)
        if not serializer.is_valid():
            return Response({"class": f"{self.__class__}", "method": "put", "msg": serializer.errors}, status=400)
        if serializer.validated_data.get("id"):
            return Response({"class": f"{self.__class__}", "method": "put", "msg": "该接口不需要添加id参数"}, status=400)
        serializer.save()
        return Response({"class": f"{self.__class__}", "method": "put", "data": "更新项目成功"})

    def delete(self, request, pk):
        result = self.get_object().delete()
        if result[0] == 0:
            return Response({"class": f"{self.__class__}", "method": "delete", "data": "项目不存在"})
        return Response({"class": f"{self.__class__}", "method": "delete", "data": "项目删除成功"})
