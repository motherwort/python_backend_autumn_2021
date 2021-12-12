# from django.core.exceptions import SuspiciousOperation
from django.shortcuts import render
from django.http.response import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_GET
from elasticsearch_dsl import Q
from application.common import get_document, get_serializer


def home(request):
    return render(request, 'forum/home.html')


def login(request):
    return render(request, 'forum/index.html')


def search(app_label):
    modelDocument = get_document(app_label)
    modelSerializer = get_serializer(app_label)

    @require_GET
    def search_model(request): #было query=None
        fields = modelDocument.search_allowed_fields
        q = Q()
        query = request.GET.get('q', None)
        if query:
            q &= Q('multi_match', query=query, fields=fields)
        for key in request.GET:
            if key in fields:
                q &= Q('match', **{key: request.GET[key]})
            elif key != 'q':
                message = f'Invalid key is in query string: {key}'
                return JsonResponse({'msg': 'error', 'msg_info': message})
        s = modelDocument.search().query(q)
        queryset = s.to_queryset()
        serializer = modelSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)
    return search_model

