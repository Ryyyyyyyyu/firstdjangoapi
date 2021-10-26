from rest_framework import views
from rest_framework.response import Response
from rest_framework import generics
from django.contrib.auth.models import User

from .serializers import RegisterSerializer
# Create your views here.


class UserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class UserExistCountView(views.APIView):

    def get(self, request, username):
        count = User.objects.filter(username=username).count()
        return Response({'username': username, 'count': count})


class EmailExistCountView(views.APIView):

    def get(self, request, email):
        count = User.objects.filter(email=email).count()
        return Response({'email': email, 'count': count})
