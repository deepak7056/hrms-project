from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from tasks.models import DailyTaskReport, Task
from django.contrib.auth import get_user_model
import pandas as pd
import json
from datetime import datetime
from django.db import connection, transaction
from django.db.utils import IntegrityError
from django.core.management import call_command


User = get_user_model()

@login_required
def upload_report(request):
    if request.user.role != 'admin':
        messages.error(request, 'Only admins can upload reports')
        return redirect('index')
    
    if request.method == 'POST' and request.FILES.get('excel_file'):
        try:
            excel_file = request.FILES['excel_file']
            
            # Delete with foreign key disabled
            with connection.cursor() as cursor:
                cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
                cursor.execute("DELETE FROM tasks_task")
                cursor.execute("DELETE FROM daily_task_reports")
                cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
            
            # Create new report
            report = DailyTaskReport.objects.create(
                uploaded_by=request.user,
                excel_file=excel_file
            )
            
            # Read Excel file
            df = pd.read_excel(excel_file)
            
            # Find assign column
            assign_column = None
            for col in df.columns:
                if 'assign' in col.lower() and 'to' in col.lower():
                    assign_column = col
                    break
            
            # Create tasks
            for index, row in df.iterrows():
                row_data = {}
                for col in df.columns:
                    value = row[col]
                    row_data[col] = None if pd.isna(value) else str(value)
                
                task = Task.objects.create(
                    report=report,
                    original_data=row_data
                )
                
                # Assign if username found
                if assign_column and row[assign_column] and not pd.isna(row[assign_column]):
                    username = str(row[assign_column]).strip()
                    try:
                        user = User.objects.get(username=username)
                        task.assigned_to = user
                        task.save()
                    except:
                        pass
            
            messages.success(request, f'Report uploaded! {len(df)} tasks imported.')
            return redirect('today_reports')
            
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    return render(request, 'upload_report.html')