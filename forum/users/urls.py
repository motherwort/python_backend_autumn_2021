from django.urls import include, path
from users.views import create_user, delete_user, edit_user, get_user_details_name, get_user_page, get_user_list


urlpatterns = [
    path('new/', create_user, name='new_user'),
    path('', get_user_list, name='users'),
    path('<str:username>/', get_user_page, name='user_page'),
    path('<str:username>/details', get_user_details_name, name='user_details'),
    path('<str:username>/edit/', edit_user, name='user_edit'),
    path('<str:username>/delete/', delete_user, name='user_delete'),
]
