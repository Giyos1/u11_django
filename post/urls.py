from django.urls import path
from post.views import post_list, post_create, post_update, post_delete

app_name = 'post'
urlpatterns = [
    path('list/', post_list, name='list'),
    path('create/', post_create, name='create'),
    path('update/<int:id>/', post_update, name='update'),
    path('delete/<int:id>/', post_delete, name='delete'),
]
