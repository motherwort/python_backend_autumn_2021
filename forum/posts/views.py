from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from application.common import require_authentication
from posts.serializers import PostSerializer
from posts.models import Post
from posts.tasks import _send_dict_mail, send_dict_mail


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

    @require_authentication
    def create(self, request):
        serializer = PostSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        post = serializer.save()
        msg = {
            'msg': 'Post created',
            'post_data': serializer.data
        }
        send_dict_mail(
            subject=msg['msg'], 
            dict=msg['post_data'],
            from_email=post.user.email
        )
        return Response(msg)

    @require_authentication
    def update(self, request, pk=None):
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, pk=pk)

        if request.user != post.user:
            raise PermissionDenied

        serializer = PostSerializer(post, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        post = serializer.save()

        msg = {
            'msg': 'Post updated',
            'post_data': serializer.data
        }
        send_dict_mail(
            subject=msg['msg'], 
            dict=msg['post_data'],
            from_email=post.user.email
        )
        return Response(msg)

    # TODO upvotes
    @require_authentication
    @action(detail=True, methods=['post'])
    def upvote(self, request, pk=None):
        raise NotImplementedError
    
    @require_authentication
    def destroy(self, request, pk=None):
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, pk=pk)

        if request.user != post.user:
            raise PermissionDenied
            
        serializer = PostSerializer(post)
        msg = {
            'msg': 'Post deleted',
            'post_data': serializer.data
        }
        post.is_deleted = True
        post.save()
        return Response(msg)
