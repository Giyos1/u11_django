from django.db import models

from accounts.models import User
from common.models import BaseModel


def user_upload_path(instance, filename):
    if instance.created_by:
        return f'user/{instance.user.id}/{filename}'
    else:
        return (
            f'all_users/'
            f'/{filename}'
        )


class Document(BaseModel):
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to=user_upload_path)
    image = models.ImageField(upload_to='img/', null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'document'
