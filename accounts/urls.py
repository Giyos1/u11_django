from django.urls import path, include

from accounts import views
from django.contrib.auth import views as auth_views

# app_name = 'accounts'
urlpatterns = [
    # path('', include('allauth.urls')),
    path('google/', views.google_redirect, name='google_redirect'),
    path('google/login/callback/', views.google_callback, name='google_callback'),
    path('register/', views.register, name='register'),
    path('login/', views.login_, name='login'),
    path('logout/', views.logout_, name='logout'),

    # forgot password
    path('forgot-password/',
         auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset_form.html',
             # success_url=reverse_lazy('accounts:password_reset_done')
         ), name='password_reset'),

    # 2) "Email yuborildi" xabari
    path('forgot-password/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'
         ), name='password_reset_done'),

    # 3) Yangi parol kiritish (email'dagi link orqali)
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html'
         ), name='password_reset_confirm'),

    # 4) Muvaffaqiyat sahifasi
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'
         ), name='password_reset_complete'),

    # forgot_password_custom
    path('forgot-password_custom/', views.ForgotPasswordView.as_view(), name='forgot_password'),
    path('restore_password/', views.RestoreView.as_view(), name='restore_password'),
]
