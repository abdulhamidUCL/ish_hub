from django.contrib import admin

from .models import Job

# Register your models here.
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'city', 'employment_type', 'is_active', 'deadline', 'created_at')
    list_filter = ('employment_type', 'is_active', 'city', 'category')
    search_fields = ('title', 'description', 'city', 'category', 'company__name')
    ordering = ('-created_at',)