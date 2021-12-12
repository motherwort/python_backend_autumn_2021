from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from application.views import search
from pools.views import PoolViewSet
from posts.views import PostViewSet
from threads.views import ThreadViewSet
from users.views import UserViewSet


router = DefaultRouter()
router.register(r'pools', PoolViewSet, basename='pools')
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'threads', ThreadViewSet, basename='threads')
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path(r'pools/search/', search('pools'), name='search_pools'),
    path(r'posts/search/', search('posts'), name='search_posts'),
    path(r'threads/search/', search('threads'), name='search_threads'),
    path(r'users/search/', search('users'), name='search_users'),
    # re_path(r'pools/search/(?P<query>[^?]*)', search('pools'), name='search_pools'),
]

urlpatterns = urlpatterns + router.urls
