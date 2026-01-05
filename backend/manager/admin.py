from django.contrib import admin
from .models import Manager

@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ('manager_sid', 'manager_type', 'join_date')
    raw_id_fields = ('manager_sid',)
    list_filter = ('manager_type',)
    search_fields = ('manager_sid__sid', 'manager_sid__name')
    fields = ('manager_sid', 'manager_type', 'manager_last_activity')
    readonly_fields = ('manager_last_activity',)