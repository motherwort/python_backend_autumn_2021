from django.shortcuts import redirect, render


def home(request):
    return render(request, 'forum/home.html')


def login(request):
    return render(request, 'forum/index.html')
