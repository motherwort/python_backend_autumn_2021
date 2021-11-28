from rest_framework import urlpatterns
from rest_framework.routers import DefaultRouter
from pools.views import PoolViewSet
from posts.views import PostViewSet
from threads.views import ThreadViewSet
from users.views import UserViewSet


router = DefaultRouter()
router.register(r'pools', PoolViewSet, basename='pools')
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'threads', ThreadViewSet, basename='threads')
router.register(r'users', UserViewSet, basename='users')

urlpatterns = router.urls
