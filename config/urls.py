from django.contrib import admin
from django.urls import path, include

from books.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('books/', include('books.urls')),
    path('post/', include('post.urls')),
    path('accounts/', include('accounts.urls')),
    path('transaction/', include('transaction.urls')),
    path('', home),
]
