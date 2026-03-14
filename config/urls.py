from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from books.views import home
from config import settings
from django.conf.urls.i18n import i18n_patterns

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('books/', include('books.urls')),
    path('post/', include('post.urls')),
    path('accounts/', include('accounts.urls')),
    path('transaction/', include('transaction.urls')),
    path('', home),
    path('file/', include('file.urls')),
    path('i18n/',
         include('django.conf.urls.i18n')),
    path(
        'rosetta/',
        include('rosetta.urls')
    ),
)

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
