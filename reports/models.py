from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class DailyReport(models.Model):
    date = models.DateField()
    excel_file = models.FileField(upload_to='reports/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Report for {self.date}"
    
    class Meta:
        db_table = 'daily_reports'
        ordering = ['-date']