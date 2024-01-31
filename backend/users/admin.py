from django.contrib import admin
from .models import User

@admin.register(User)
class NameAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'date_joined', 'last_login', 'is_active', 'is_staff', 'is_superuser')