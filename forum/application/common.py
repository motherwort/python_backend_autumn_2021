from django.http.response import HttpResponseNotAllowed


def check_method(allowed_method):
    def decorator(func):
        def wrapped(request, *args, **kwargs):
            if request.method != allowed_method:
                print(f"{request.method}!={allowed_method}")
                print('i am the problem')
                return HttpResponseNotAllowed([allowed_method])
            else:
                print(f"no problem: {allowed_method}")
                return func(request, *args, **kwargs)
        wrapped.__name__ = func.__name__
        return wrapped
    return decorator


def check_POST(func):
    def decorator(request, *args, **kwargs):
        if request.method != 'POST':
            return HttpResponseNotAllowed(['POST'])
        else:
            return func(request, *args, **kwargs)
    decorator.__name__ = func.__name__
    return decorator


def check_GET(func):
    def decorator(request, *args, **kwargs):
        if request.method != 'GET':
            return HttpResponseNotAllowed(['GET'])
        else:
            return func(request, *args, **kwargs)
    decorator.__name__ = func.__name__
    return decorator
