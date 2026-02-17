from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

from accounts.models import RoleChoice


def login_required(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            return redirect('accounts:login')
    return wrapper


def admin(func):
    def wrapper(request, *args, **kwargs):
        if request.user.role != RoleChoice.ADMIN:
            raise PermissionDenied
        return func(request, *args, **kwargs)

    return wrapper


def poster(func):
    def wrapper(request, *args, **kwargs):
        if request.user.role != RoleChoice.POSTER:
            raise PermissionDenied
        return func(request, *args, **kwargs)
    return wrapper
