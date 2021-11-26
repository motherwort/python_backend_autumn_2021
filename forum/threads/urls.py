from django.urls import include, path
from threads.views import thread_detail


urlpatterns = [
    path('thread<int:thread_id>', thread_detail, name='thread_detail')
]
