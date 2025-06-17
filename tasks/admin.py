from django.contrib import admin
from .models import Task, DailyTaskReport

@admin.register(DailyTaskReport)
class DailyTaskReportAdmin(admin.ModelAdmin):
    list_display = ('uploaded_date', 'uploaded_by')
    list_filter = ('uploaded_date',)
    readonly_fields = ('uploaded_date',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'report', 'assigned_to', 'self_assigned_date')
    list_filter = ('assigned_to', 'self_assigned_date')
    search_fields = ('original_data',)
    readonly_fields = ('original_data',)