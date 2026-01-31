from django.urls import path

from books.views import home, book_list, book_detail, book_delete, book_create, book_create_post, book_update

urlpatterns = [
    path('', home),
    path('list/', book_list, name='book_list'),
    path('detail/<int:pk>/', book_detail, name='book_detail'),
    path('delete/<int:pk>/', book_delete, name='book_delete'),
    path('create/', book_create, name='book_create'),  # formani ochib beropti
    path('create_post/', book_create_post, name='book_create_post'),  # formani saqlashi kerak
    path('update/<int:pk>/', book_update, name='book_update'),  # formani saqlashi kerak
]
