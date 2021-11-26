from django.urls import include, path
from pools.views import create_pool, list_pools, pool_detail


urlpatterns = [
    path('', list_pools, name='list_pools'),
    path('new', create_pool, name='create_pool'),
    path('pool<int:pool_id>', pool_detail, name='pool_detail'),
]
