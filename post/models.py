from django.db import models


class StatusChoice(models.TextChoices):
    DRAFT = 'draft'
    PUBLISHED = 'published'


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
    status = models.CharField(max_length=200, choices=StatusChoice, default=StatusChoice.DRAFT)
    author = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True)

    objects = DeletedManager()

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'posts'
        permissions = [
            ("moderate", "Can Moderate Post"),
        ]
