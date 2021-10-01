import json
from django.views import View
from django.http import JsonResponse
from .models import InterfacesModel
# Create your views here.


class InterfacesView(View):

    def get(self):
        pass

    def post(self, request):
        try:
            data = json.loads(request.body)
        except Exception as e:
            return JsonResponse({"msg": str(e)})
        obj = InterfacesModel.objects.create(**data)
        print(obj)
        return JsonResponse({"method": "post", "class": "interfaces"})
