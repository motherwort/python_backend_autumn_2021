from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from threads.serializers import ThreadSerializer
from threads.models import Thread
from pools.models import Pool


class ThreadViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Thread.objects.all()
        serializer = ThreadSerializer(queryset, many=True)
        return Response(serializer.data) 

    def retrieve(self, request, pk=None):
        queryset = Thread.objects.all()
        pool = get_object_or_404(queryset, pk=pk)
        serializer = ThreadSerializer(pool)
        return Response(serializer.data)

    # TODO создавать от имени авторизованного пользователя
    def create(self, request):
        pool_id = request.data.get('pool', None)
        get_object_or_404(Pool.objects.all(), pk=pool_id)

        # request.data['creator'] = creator
        serializer = ThreadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        msg = {
            'msg': 'Thread created',
            'thread_data': serializer.data
        }
        return Response(msg)

    # TODO проверка на создателя
    # и/или не изменение, но создание объекта poll за изменение
    def update(self, request, pk=None):
        queryset = Thread.objects.all()
        thread = get_object_or_404(queryset, pk=pk)

        serializer = ThreadSerializer(thread, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        serializer = ThreadSerializer(thread)
        msg = {
            'msg': 'Thread updated',
            'thread_data': serializer.data
        }
        return Response(msg)

    # TODO проверка на создателя
    # и/или создание голосования за удаление
    def destroy(self, request, pk=None):
        queryset = Thread.objects.all()
        thread = get_object_or_404(queryset, pk=pk)
        serializer = ThreadSerializer(thread)
        thread.delete()
        msg = {
            'msg': 'Thread deleted',
            'thread_data': serializer.data
        }
        return Response(msg)
