from django.http.response import Http404, JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
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

    # TODO указать авторизованного пользователя как создателя
    def create(self, request):
        # request.data['creator'] = creator
        serializer = PoolSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        msg = {
            'msg': 'Pool created',
            'pool_data': serializer.data
        }
        return Response(msg)

    # TODO проверка на создателя
    # и/или не изменение, но создание объекта poll за изменение
    def update(self, request, pk=None):
        queryset = Pool.objects.all()
        pool = get_object_or_404(queryset, pk=pk)

        serializer = PoolSerializer(pool, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        msg = {
            'msg': 'Pool updated',
            'pool_data': serializer.data
        }
        return Response(msg)

    # TODO добавить авторизованного пользователя в список участников
    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        raise NotImplementedError

    # TODO проверка на создателя
    # и/или создание голосования за удаление
    def destroy(self, request, pk=None):
        queryset = Pool.objects.all()
        pool = get_object_or_404(queryset, pk=pk)
        serializer = PoolSerializer(pool)
        pool.delete()
        msg = {
            'msg': 'Pool deleted',
            'pool_data': serializer.data
        }
        return Response(msg)
