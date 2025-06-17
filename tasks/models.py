from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import JSONField  # Use this for both PostgreSQL and MySQL

User = get_user_model()

class DailyTaskReport(models.Model):
    """Stores the uploaded Excel file"""
    uploaded_date = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    excel_file = models.FileField(upload_to='task_reports/')
    
    class Meta:
        ordering = ['-uploaded_date']
        db_table = 'daily_task_reports'
    
    def __str__(self):
        return f"Report uploaded on {self.uploaded_date.strftime('%Y-%m-%d %H:%M')}"

class Task(models.Model):
    """Stores individual tasks from Excel with flexible structure"""
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )
    
    report = models.ForeignKey(DailyTaskReport, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)
    original_data = models.JSONField(default=dict)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='self_assigned_tasks')
    self_assigned_date = models.DateTimeField(null=True, blank=True)
    
    # Add these new fields
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'tasks'
    
    def __str__(self):
        return f"Task from report {self.report.id}"