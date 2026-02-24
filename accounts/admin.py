from django.contrib import admin

from accounts.models import User, Card


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


admin.site.register(Card)
