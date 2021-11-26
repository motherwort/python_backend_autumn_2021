from django.http.response import JsonResponse
from django.shortcuts import render


def thread_detail(request, pool_id, thread_id):
    return JsonResponse({
        'pool': pool_id,
        'thread': thread_id
    })
