from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

class AccountAdmin(UserAdmin):
    list_display = ('email', 'user_role', 'date_joined', 'last_login', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('email',)
    readonly_fields = ('date_joined', 'last_login')
    ordering = ('-date_joined',)  # Default ordering by date_joined descending

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account, AccountAdmin)
