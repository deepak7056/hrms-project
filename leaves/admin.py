from django.contrib import admin
from .models import LeaveType, Leave

@admin.register(LeaveType)
class LeaveTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'days_allowed')
    search_fields = ('name',)

@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ('employee', 'leave_type', 'start_date', 'end_date', 'status', 'applied_date')
    list_filter = ('status', 'leave_type', 'applied_date')
    search_fields = ('employee__employee_id', 'employee__first_name', 'employee__last_name')
    date_hierarchy = 'applied_date'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.role == 'manager':
            return qs.filter(employee__manager=request.user)
        return qs