from django.urls import path

from post.views import post_list, post_create, post_update, post_delete, PostListView, PostCreateView, PostUpdateView, \
    PostDeleteView

app_name = 'post'
urlpatterns = [
    # path('list/', post_list, name='list'),
    path('list/', PostListView.as_view(), name='list'),
    # path('create/', post_create, name='create'),
    path('create/', PostCreateView.as_view(), name='create'),
    # path('update/<int:id>/', post_update, name='update'),
    path('update/<int:id>/', PostUpdateView.as_view(), name='update'),
    # path('delete/<int:id>/', post_delete, name='delete'),
    path('delete/<int:id>/', PostDeleteView.as_view(), name='delete'),
]
