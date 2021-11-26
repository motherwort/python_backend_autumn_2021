from django.http.response import Http404, JsonResponse, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from application.common import check_method
from users.models import User


@check_method('POST')
def create_user(request):
    User.objects.create(
        username=request.POST['username'],
        email=request.POST['email'],
        password=request.POST['password'],
        name=request.POST['name'],
        user_info=request.POST['user_info']
    )
    return redirect('index')


@check_method('POST')
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


@check_method('GET')
def get_user_details_id(request, user_id):
    return __get_user_details(id=user_id)


@check_method('GET')
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


@check_method('GET')
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


@check_method('GET')
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


@check_method('POST')
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
