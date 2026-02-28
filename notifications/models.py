from django.db import models


class Notification(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    to_user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'notifications'
