from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from posts.serializers import PostSerializer
from posts.models import Post
from threads.models import Thread
from users.models import User


class PostViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Post.objects.filter(is_deleted=False)
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data) 

    def retrieve(self, request, pk=None):
        queryset = Post.objects.filter(is_deleted=False)
        post = get_object_or_404(queryset, pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    # TODO создавать от имени авторизованного пользователя
    def create(self, request):
        thread_id = request.data['thread']
        get_object_or_404(Thread.objects.all(), pk=thread_id)

        user_id = request.data['user']
        get_object_or_404(User.objects.all(), pk=user_id)
        # request.data['creator'] = creator ### вместо того, что выше

        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        msg = {
            'msg': 'Post created',
            'post_data': serializer.data
        }
        return Response(msg)

    def update(self, request, pk=None):
        # TODO проверка на создателя
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, pk=pk)

        serializer = PostSerializer(post, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        msg = {
            'msg': 'Post updated',
            'post_data': serializer.data
        }
        return Response(msg)

    @action(detail=True, methods=['post'])
    def upvote(self, request, pk=None):
        # TODO добавить авторизованного пользователя в список участников
        raise NotImplementedError

    def destroy(self, request, pk=None):
        # TODO проверка на создателя
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, pk=pk)
        serializer = PostSerializer(post)
        post.is_deleted = True
        post.save()
        msg = {
            'msg': 'Post deleted',
            'post_data': serializer.data
        }
        return Response(msg)
