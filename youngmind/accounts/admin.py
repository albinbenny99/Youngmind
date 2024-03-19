from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

class AccountAdmin(UserAdmin):
    def first_name(self, obj):
        return obj.profile.first_name if obj.profile else ""

    def last_name(self, obj):
        return obj.profile.last_name if obj.profile else ""

    def username(self, obj):
        return obj.profile.username if obj.profile else ""

    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'date_joined', 'is_active')
    list_display_links = ('email', 'first_name', 'last_name')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account, AccountAdmin)
