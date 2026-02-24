from django.urls import path

from transaction import views

app_name = 'accounts'
urlpatterns = [
    path('', views.transaction_, name='transaction'),

]
