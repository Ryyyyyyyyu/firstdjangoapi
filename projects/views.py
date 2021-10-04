import json

from django.http import JsonResponse
from django.views import View

from .models import ProjectsModel
from .serializers import ProjectSerializer


# Create your views here.


class ProjectsView(View):

    def get(self, request):
        objs = ProjectsModel.objects.all()
        # data_list = []
        # for obj in objs:
        #     obj: ProjectsModel
        #     data = {
        #         "id": obj.id,
        #         "name": obj.name,
        #         "desc": obj.desc,
        #         "create_time": obj.create_time,
        #         "update_time": obj.update_time
        #     }
        #     data_list.append(data)
        ser = ProjectSerializer(instance=objs, many=True)

        return JsonResponse({"class": f"{self.__class__}", "method": "get", "data": ser.data})

    def post(self, request):
        data: dict
        try:
            data = json.loads(request.body)
        except Exception as e:
            return JsonResponse({"msg": str(e)})
        # if data.get('id'):
        #     if type(data.get('id')) == str and not data.get('id').isdigit():
        #         return JsonResponse({"class": f"{self.__class__}", "method": "post", "data": "项目id参数类型错误"})
        #     objs = ProjectsModel.objects.filter(id=data.get('id'))
        #     if objs.count() > 0:
        #         return JsonResponse({"class": f"{self.__class__}", "method": "post", "data": "项目id已存在"})
        # if not data.get('name') or not data.get('leader'):
        #     return JsonResponse({"class": f"{self.__class__}", "method": "post", "data": "入参错误，请检查"})
        # elif len(data.get('name')) == 0 or len(data.get('name')) > 50 or len(data.get('leader')) == 0 or len(
        #         data.get('leader')) > 20 or len(data.get('desc')) > 200:
        #     return JsonResponse({"class": f"{self.__class__}", "method": "post", "data": "入参长度超过限制"})

        # obj = ProjectsModel.objects.create(**data)
        ser = ProjectSerializer(data=data)
        if not ser.is_valid():
            return JsonResponse({"class": f"{self.__class__}", "method": "post", "msg": ser.errors}, status=400)

        obj = ProjectsModel.objects.create(**ser.validated_data)

        return JsonResponse({"class": f"{self.__class__}", "method": "post", "data": "创建项目成功"}, status=201)

    def put(self, request):
        try:
            data = json.loads(request.body)
        except Exception as e:
            return JsonResponse({"msg": str(e)})
        # if data.get('id'):
        #     if type(data.get('id')) == str and not data.get('id').isdigit():
        #         return JsonResponse({"class": f"{self.__class__}", "method": "put", "data": "项目id参数类型错误"})
        #     elif not data.get('name') or not data.get('leader'):
        #         return JsonResponse({"class": f"{self.__class__}", "method": "put", "data": "入参错误，请检查"})
        #     elif len(data.get('name')) == 0 or len(data.get('name')) > 50 or len(data.get('leader')) == 0 or len(
        #             data.get('leader')) > 20 or len(data.get('desc')) > 200:
        #         return JsonResponse({"class": f"{self.__class__}", "method": "put", "data": "入参长度超过限制"})
        #     objs = ProjectsModel.objects.filter(id=data.get('id'))
        #     if objs.count() == 0:
        #         return JsonResponse({"class": f"{self.__class__}", "method": "put", "data": "项目id不存在"})
        #
        #     obj = objs.update(**data)
        #
        #     return JsonResponse({"class": f"{self.__class__}", "method": "put", "data": "更新项目成功"})
        # else:
        #     return JsonResponse({"class": f"{self.__class__}", "method": "put", "data": "项目id必传"})
        try:
            objs = ProjectsModel.objects.filter(id=data.get('id'))
        except Exception as e:
            return JsonResponse({"class": f"{self.__class__}", "method": "put", "msg": str(e)}, status=400)
        ser = ProjectSerializer(data=data)
        if ser.is_valid():
            return JsonResponse({"class": f"{self.__class__}", "method": "put", "msg": ser.errors}, status=400)
        objs.update(**ser.validated_data)

        return JsonResponse({"class": f"{self.__class__}", "method": "put", "data": "更新项目成功"})

    def delete(self, request):
        ProjectsModel.objects.all().delete()
        return JsonResponse({"class": f"{self.__class__}", "method": "delete", "data": "删除所有项目成功"})


class ProjectDetailsViews(View):

    def get(self, request, pk):
        try:
            objs = ProjectsModel.objects.filter(id=pk)
        except Exception as e:
            return JsonResponse({'msg': str(e)}, status=400)

        # if objs.count() > 0:
        #     obj: ProjectsModel
        #     obj = objs.first()
        #     data = {
        #         "id": obj.id,
        #         "name": obj.name,
        #         "desc": obj.desc,
        #         "create_time": obj.create_time,
        #         "update_time": obj.update_time
        #     }
        #     return JsonResponse({"class": f"{self.__class__}", "method": "get", "data": data})
        # else:
        #     return JsonResponse({"class": f"{self.__class__}", "method": "get", "msg": "项目id不存在"})
        ser = ProjectSerializer(instance=objs)
        if ser.is_valid():
            return JsonResponse({"class": f"{self.__class__}", "method": "get", "msg": ser.errors}, status=400)
        objs.update(**ser.validated_data)
        return JsonResponse({"class": f"{self.__class__}", "method": "get", "data": ''})

    def post(self, request, pk):
        data: dict
        try:
            data = json.loads(request.body)
        except Exception as e:
            return JsonResponse({"msg": str(e)}, status=400)
        if ProjectsModel.objects.filter(id=pk).count() > 0:
            return JsonResponse({"class": f"{self.__class__}", "method": "post", "msg": "项目id已存在"}, status=400)
        ser = ProjectSerializer(data=data)
        if not ser.is_valid():
            return JsonResponse({"class": f"{self.__class__}", "method": "post", "msg": ser.errors}, status=400)

        ProjectsModel.objects.create(**ser.validated_data)

        return JsonResponse({"class": f"{self.__class__}", "method": "post", "data": "创建项目成功"}, status=201)

    def put(self, request, pk):
        try:
            objs = ProjectsModel.objects.filter(id=pk)
            data = json.loads(request.body)
        except Exception as e:
            return JsonResponse({"msg": str(e)})

        if objs.count() == 0:
            return JsonResponse({"class": f"{self.__class__}", "method": "put", "data": "项目id不存在"})
        if not data.get('name') or not data.get('leader'):
            return JsonResponse({"class": f"{self.__class__}", "method": "put", "data": "入参错误，请检查"})
        elif len(data.get('name')) == 0 or len(data.get('name')) > 50 or len(data.get('leader')) == 0 or len(
                data.get('leader')) > 20 or len(data.get('desc')) > 200:
            return JsonResponse({"class": f"{self.__class__}", "method": "put", "data": "入参长度超过限制"})

        obj = objs.update(**data)

        return JsonResponse({"class": f"{self.__class__}", "method": "put", "data": "更新项目成功"})

    def delete(self, request, pk):
        ProjectsModel.objects.filter(id=pk).delete()
        return JsonResponse({"class": f"{self.__class__}", "method": "delete", "data": "项目删除成功"})
