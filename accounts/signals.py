from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import User
from notifications.models import Notification


@receiver(post_save, sender=User)
def change_user_profile(sender, instance, created, **kwargs):
    if created:  # Yangi foydalanuvchi yaratildimi?
        print(f'Creating user {instance}')
    else:
        if not instance.is_active:
            Notification.objects.create(to_user=instance, title='bloklandingiz', content='bloklandingiz')
        else:
            Notification.objects.create(to_user=instance, title='faolishtirildingiz', content='faolishtirilingiz')
