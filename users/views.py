from django.shortcuts import render
from rest_framework import generics
# Create your views here.


class Users(generics.CreateAPIView):
    queryset = None
    serializer_class = None
