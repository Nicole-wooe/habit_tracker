from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            'Telegram',
            {
                'fields': ('telegram_chat_id',),
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            'Telegram',
            {
                'fields': ('telegram_chat_id',),
            },
        ),
    )
