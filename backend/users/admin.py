from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Muestra la matrícula en el formulario de edición y en el de alta del admin
    fieldsets = UserAdmin.fieldsets + (
        ('Datos de la biblioteca', {'fields': ('matricula',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Datos de la biblioteca', {'fields': ('email', 'matricula')}),
    )
    list_display = ('email', 'username', 'matricula', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'username', 'matricula', 'first_name', 'last_name')
    ordering = ('email',)
