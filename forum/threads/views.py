from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from application.common import require_authentication
from threads.serializers import ThreadSerializer
from threads.models import Thread


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

    @require_authentication
    def create(self, request):
        serializer = ThreadSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        msg = {
            'msg': 'Thread created',
            'thread_data': serializer.data
        }
        return Response(msg)

    # TODO не изменение, но создание объекта poll за изменение
    @require_authentication
    def update(self, request, pk=None):
        queryset = Thread.objects.all()
        thread = get_object_or_404(queryset, pk=pk)

        if request.user != thread.creator:
            raise PermissionDenied

        serializer = ThreadSerializer(thread, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        serializer = ThreadSerializer(thread)
        msg = {
            'msg': 'Thread updated',
            'thread_data': serializer.data
        }
        return Response(msg)

    # TODO создание голосования за удаление
    @require_authentication
    def destroy(self, request, pk=None):
        queryset = Thread.objects.all()
        thread = get_object_or_404(queryset, pk=pk)

        if request.user != thread.creator:
            raise PermissionDenied

        serializer = ThreadSerializer(thread)
        msg = {
            'msg': 'Thread deleted',
            'thread_data': serializer.data
        }
        thread.delete()
        return Response(msg)
