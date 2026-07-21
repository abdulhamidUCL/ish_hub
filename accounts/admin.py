from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'city', 'phone', 'created_at')
    list_filter = ('role', 'city')
    search_fields = ('user__username', 'user__email', 'phone', 'city')


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'created_at', 'updated_at')
    search_fields = ('user__username', 'user__email', 'title', 'skills')