from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from application.common import require_authentication
from users.serializers import UserSerializer
from users.models import User


class UserViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data) 

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        pool = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(pool)
        return Response(serializer.data)

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        msg = {
            'msg': 'User created',
            'user_data': serializer.data
        }
        return Response(msg)
    
    @require_authentication
    def update(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)

        if request.user != user:
            raise PermissionDenied
            
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        msg = {
            'msg': 'User updated',
            'user_data': serializer.data
        }
        return Response(msg)
    
    @require_authentication
    def destroy(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)

        if request.user != user:
            raise PermissionDenied

        pwd = request.data.get('password', None)
        if (pwd is None) or (pwd != user.password):
            raise PermissionDenied
        serializer = UserSerializer(user)
        msg = {
            'msg': 'User deleted',
            'user_data': serializer.data
        }
        user.delete()
        return Response(msg)
