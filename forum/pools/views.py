from django.http.response import Http404, HttpResponseBadRequest, JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from application.common import check_method
from pools.models import Pool
from users.models import User


def __pool_to_dict(pool):
    dct = {
        'id': pool.id,
        'name': pool.name,
        'description': pool.description,
        'creation time': pool.created
    }
    return dct


@check_method('POST')
def create_pool(request):
    pool = Pool(
        name=request.POST['name'],
        description=request.POST['description']
    )
    pool.save()
    return JsonResponse(__pool_to_dict(pool))


@check_method('GET')
def list_pools(request):
    pool_list = Pool.objects.all()
    data = [
        __pool_to_dict(pool) for pool in pool_list
    ]
    return JsonResponse({'pools': data})


@check_method('GET')
def pool_detail(request, pool_id):
    try:
        pool = Pool.objects.get(id=pool_id)
    except Pool.DoesNotExist:
        raise Http404
    return JsonResponse(__pool_to_dict(pool))


@check_method('POST')
def edit_pool(request):
    raise NotImplementedError


@check_method('POST')
def join_pool(request):
    raise NotImplementedError
