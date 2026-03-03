from django.urls import path
from .views import upload, file_list

urlpatterns = [
    path('', upload, name='upload'),
    path('list/', file_list, name='file_list'),
]
