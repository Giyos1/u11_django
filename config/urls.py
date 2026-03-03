from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from books.views import home
from config import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('books/', include('books.urls')),
    path('post/', include('post.urls')),
    path('accounts/', include('accounts.urls')),
    path('transaction/', include('transaction.urls')),
    path('', home),
    path('file/', include('file.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
