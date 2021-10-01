import json

from django.db.models import Q
from django.http import JsonResponse
from django.db import connection
from django.views import View
from .models import ProjectsModel
from interfaces.models import InterfacesModel

# Create your views here.


class ProjectsView(View):

    def get(self, request):
        objs = ProjectsModel.objects.all()
        data_list = []
        for obj in objs:
            obj: ProjectsModel
            data = {
                "id": obj.id,
                "name": obj.name,
                "desc": obj.desc,
                "create_time": obj.create_time,
                "update_time": obj.update_time
            }
            data_list.append(data)
        return JsonResponse({"class": f"{self.__class__}", "method": "get", "data": data_list})

    def post(self, request):
        data: dict
        try:
            data = json.loads(request.body)
        except Exception as e:
            return JsonResponse({"msg": str(e)})
        if not data.get('id').isdigit():
            return JsonResponse({"class": f"{self.__class__}", "method": "post", "data": "项目id参数类型错误"})
        if data.get('id'):
            objs = ProjectsModel.objects.filter(id=data.get('id'))
            if objs.count() > 0:
                return JsonResponse({"class": f"{self.__class__}", "method": "post", "data": "项目id已存在"})

        obj = ProjectsModel.objects.create(**data)

        return JsonResponse({"class": f"{self.__class__}", "method": "post", "data": "创建id为{}的项目成功".format(obj.id)})

    def put(self, request):
        return JsonResponse({"method": "put"})

    def delete(self, request):
        return JsonResponse({"method": "delete"})


class ProjectDetailsViews(View):

    def get(self, request, pk):
        objs = ProjectsModel.objects.filter(id=pk)
        if objs.count() > 0:
            obj: ProjectsModel
            obj = objs.first()
            data = {
                "id": obj.id,
                "name": obj.name,
                "desc": obj.desc,
                "create_time": obj.create_time,
                "update_time": obj.update_time
            }
            return JsonResponse({"class": f"{self.__class__}", "method": "get", "data": data})
        else:
            return JsonResponse({"class": f"{self.__class__}", "method": "get", "msg": "项目id不存在"})

    def post(self, request):
        return JsonResponse({"class": f"{self.__class__}", "method": "post"})
