from django.contrib import admin

from account.models import CustomUser


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'username', 'role', 'auth_provider']
    list_filter = ['role', 'auth_provider']


admin.site.register(CustomUser, UserAdmin)
