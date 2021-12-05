from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from application.common import require_authentication
from pools.serializers import PoolSerializer
from pools.models import Pool


class PoolViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Pool.objects.all()
        serializer = PoolSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Pool.objects.all()
        pool = get_object_or_404(queryset, pk=pk)
        serializer = PoolSerializer(pool)
        return Response(serializer.data)

    @require_authentication
    def create(self, request):
        serializer = PoolSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        msg = {
            'msg': 'Pool created',
            'pool_data': serializer.data
        }
        return Response(msg)

    # TODO не изменение, но создание объекта poll за изменение
    @require_authentication
    def update(self, request, pk=None):
        queryset = Pool.objects.all()
        pool = get_object_or_404(queryset, pk=pk)

        if request.user != pool.creator:
            raise PermissionDenied

        serializer = PoolSerializer(pool, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        msg = {
            'msg': 'Pool updated',
            'pool_data': serializer.data
        }
        return Response(msg)

    @action(detail=True, methods=['get'])
    @require_authentication
    def join(self, request, pk=None):
        queryset = Pool.objects.all()
        pool = get_object_or_404(queryset, pk=pk)
        serializer = PoolSerializer(pool)
        if request.user in pool.users.all():
            msg = {
                'msg': 'Already joined pool',
                'pool_data': serializer.data
            }
        else:
            pool.users.add(request.user)
            msg = {
                'msg': 'Joined pool',
                'pool_data': serializer.data
            }
        return Response(msg)

    @action(detail=True, methods=['get'])
    @require_authentication
    def leave(self, request, pk=None):
        queryset = Pool.objects.all()
        pool = get_object_or_404(queryset, pk=pk)
        serializer = PoolSerializer(pool)
        if request.user in pool.users.all():
            pool.users.remove(request.user)
            msg = {
                'msg': 'You have left the pool',
                'pool_data': serializer.data
            }
        else:
            msg = {
                'msg': 'Already not a member of the pool',
                'pool_data': serializer.data
            }
        return Response(msg)

    # TODO создание голосования за удаление
    @require_authentication
    def destroy(self, request, pk=None):
        queryset = Pool.objects.all()
        pool = get_object_or_404(queryset, pk=pk)

        if request.user != pool.creator:
            raise PermissionDenied
            
        serializer = PoolSerializer(pool)
        msg = {
            'msg': 'Pool deleted',
            'pool_data': serializer.data
        }
        pool.delete()
        return Response(msg)
