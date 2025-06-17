from django.contrib import admin
from .models import DailyReport

@admin.register(DailyReport)
class DailyReportAdmin(admin.ModelAdmin):
    list_display = ('date', 'uploaded_by', 'uploaded_date')
    list_filter = ('date', 'uploaded_date')
    date_hierarchy = 'date'