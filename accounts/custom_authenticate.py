from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User


def custom_authenticate(username, password):
    user = User.objects.filter(username=username).first()
    if not user:
        return None

    else:
        if check_password(password, user.password):
            return user
        else:
            return None
