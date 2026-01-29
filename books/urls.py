from django.urls import path

from books.views import home, book_list, book_detail, book_delete

urlpatterns = [
    path('', home),
    path('list/', book_list, name='book_list'),
    path('detail/<int:pk>/', book_detail, name='book_detail'),
    path('delete/<int:pk>/', book_delete, name='book_delete')
]
