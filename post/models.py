from django.db import models


class BaseQuerySet(models.QuerySet):
    def delete(self):
        self.update(is_deleted=True)


class DeletedManager(models.Manager):
    def get_queryset(self):
        return BaseQuerySet(self.model).filter(is_deleted=False)


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    objects = DeletedManager()

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'posts'
