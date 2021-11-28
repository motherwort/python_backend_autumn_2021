from functools import partial
from django.http.response import Http404, JsonResponse, HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
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
    
    def update(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk) # TODO переписать под авторизованного пользователя
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        msg = {
            'msg': 'User updated',
            'user_data': serializer.data
        }
        return Response(msg)
    
    def destroy(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk) # TODO переписать под авторизованного пользователя
        pwd = request.data.get('password', None)
        if (pwd is None) or (pwd != user.password):
            raise PermissionDenied
        serializer = UserSerializer(user)
        user.delete()
        msg = {
            'msg': 'User deleted',
            'user_data': serializer.data
        }
        return Response(msg)


@require_POST
def create_user(request):
    User.objects.create(
        username=request.POST['username'],
        email=request.POST['email'],
        password=request.POST['password'],
        name=request.POST['name'],
        user_info=request.POST['user_info']
    )
    return redirect('index')


@require_POST
def edit_user(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponseBadRequest("No user with such username.")
    if user.password == request.POST['old_password']:
        user.email = request.POST['email']
        if request.POST['new_password'] != '':
            user.password = request.POST['new_password']
        user.name = request.POST['name']
        user.user_info = request.POST['user_info']
        user.save()
        return redirect('user_page', username)
    else:
        return HttpResponseBadRequest("Wrong password.")


@require_GET
def get_user_details_id(request, user_id):
    return __get_user_details(id=user_id)


@require_GET
def get_user_details_name(request, username):
    return __get_user_details(username=username)


def __get_user_details(**kwargs):
    try:
        user = User.objects.get(**kwargs)
    except User.DoesNotExist:
        raise Http404
    user_data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'password': user.password,
        'name': user.name,
        'user_info': user.user_info,
    }
    return JsonResponse(user_data)


@require_GET
def get_user_page(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404
    data = {
        'username': user.username,
        'email': user.email,
        'name': user.name,
        'user_info': user.user_info,
    }
    return render(request, 'forum/user.html', data)


@require_GET
def get_user_list(request):
    user_list = User.objects.filter(is_active=True)
    data = [
        {
            'username': user.username,
            'email': user.email,
            'password': user.password,
            'name': user.name,
            'user_info': user.user_info,
        } for user in user_list
    ]
    return JsonResponse({'users': data})


@require_POST
def delete_user(request, username):
    password = request.POST['password']
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponseBadRequest("No user with such username.")
    if user.password == password:
        user_id = user.id
        user.delete()
        return HttpResponse(f"User {username} (user id: {user_id}) is deleted successfully.")
    else:
        return HttpResponseBadRequest("Wrong password.")
