from django.contrib import admin

from account.models import CustomUser


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'username', 'role']
    list_filter = ['role']


admin.site.register(CustomUser, UserAdmin)
