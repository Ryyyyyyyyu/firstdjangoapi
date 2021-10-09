import json

from django.http import JsonResponse
from rest_framework.response import Response
from django.views import View
from rest_framework.views import APIView
from rest_framework import filters
from rest_framework.generics import GenericAPIView

from .models import ProjectsModel

from .serializers import ProjectModelSerializer


# Create your views here.
# class ProjectsView(View):
class ProjectsView(APIView):
    queryset = ProjectsModel.objects.all()
    serializer_class = ProjectModelSerializer
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['id', 'name']

    def get(self, request):
        serializer = self.serializer_class(instance=self.queryset.all(), many=True)
        return Response({"class": f"{self.__class__}", "method": "get", "data": serializer.data})

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response({"class": f"{self.__class__}", "method": "post", "msg": serializer.errors})
        serializer.save()
        return Response({"class": f"{self.__class__}", "method": "post", "data": "创建项目成功"}, status=201)

    def put(self, request):
        try:
            objs = self.queryset.filter(id=request.data.get('id'))
        except Exception as e:
            return Response({"class": f"{self.__class__}", "method": "put", "msg": str(e)}, status=400)
        if objs.count() == 0:
            return Response({"class": f"{self.__class__}", "method": "put", "data": "项目id不存在"})
        serializer = self.serializer_class(instance=objs.first(), data=request.data)
        if not serializer.is_valid():
            return Response({"class": f"{self.__class__}", "method": "put", "msg": serializer.errors}, status=400)
        serializer.save()

        return Response({"class": f"{self.__class__}", "method": "put", "data": "更新项目成功"})

    def delete(self, request):
        self.queryset.delete()
        return Response({"class": f"{self.__class__}", "method": "delete", "data": "删除所有项目成功"})


class ProjectDetailsViews(View):
    queryset = ProjectsModel.objects.all()
    serializer_class = ProjectModelSerializer

    def get(self, request, pk):
        try:
            objs = self.queryset.filter(id=pk)
        except Exception as e:
            return JsonResponse({'msg': str(e)}, status=400)
        serializer = self.serializer_class(instance=objs, many=True)
        return Response({"class": f"{self.__class__}", "method": "get", "data": serializer.data})

    def post(self, request, pk):
        if self.queryset.filter(id=pk).count() > 0:
            return Response({"class": f"{self.__class__}", "method": "post", "msg": "项目id已存在"}, status=400)
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response({"class": f"{self.__class__}", "method": "post", "msg": serializer.errors}, status=400)
        if serializer.validated_data.get("id"):
            return Response({"class": f"{self.__class__}", "method": "post", "msg": "该接口不需要添加id参数"}, status=400)
        serializer.save()
        return Response({"class": f"{self.__class__}", "method": "post", "data": "创建项目成功"}, status=201)

    def put(self, request, pk):
        try:
            objs = self.queryset.filter(id=pk)
        except Exception as e:
            return Response({"msg": str(e)})

        serializer = self.serializer_class(instance=objs.first(), data=request.data)
        if objs.count() == 0:
            return Response({"class": f"{self.__class__}", "method": "put", "data": "项目id不存在"})
        if not serializer.is_valid():
            return Response({"class": f"{self.__class__}", "method": "put", "msg": serializer.errors}, status=400)
        if serializer.validated_data.get("id"):
            return Response({"class": f"{self.__class__}", "method": "put", "msg": "该接口不需要添加id参数"}, status=400)
        serializer.save()
        return Response({"class": f"{self.__class__}", "method": "put", "data": "更新项目成功"})

    def delete(self, request, pk):
        self.queryset.filter(id=pk).delete()
        return Response({"class": f"{self.__class__}", "method": "delete", "data": "项目删除成功"})
