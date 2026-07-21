from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'industry', 'city', 'employee_count', 'is_verified', 'created_at')
    list_filter = ('industry', 'city', 'is_verified')
    search_fields = ('name', 'owner__username', 'industry', 'city')