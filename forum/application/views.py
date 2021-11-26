from django.shortcuts import render
from users.models import User


def index(request):
    user_list = [user.username for user in User.objects.filter(is_active=True)]
    data = {'user_list': user_list}
    return render(request, 'forum/index.html', data)


def registration(request):
    return render(request, 'forum/registration.html')
