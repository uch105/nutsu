from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

#admin.site.register()
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'full_name', 'is_staff', 'is_superuser')
    search_fields = ('email', 'full_name')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name',)}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'password1', 'password2', 'is_staff', 'is_superuser')}
        ),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Newsletter)
admin.site.register(NewsletterBlock)

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'email')
    search_fields = ('user__email',)

admin.site.register(Author, AuthorAdmin)
admin.site.register(Category)
admin.site.register(Query)