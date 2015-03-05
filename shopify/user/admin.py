from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .forms import UserCreationNoPasswordForm


class UserAdminNoPassword(UserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name'),
        }),
    )
    add_form = UserCreationNoPasswordForm


admin.site.unregister(User)
admin.site.register(User, UserAdminNoPassword)
