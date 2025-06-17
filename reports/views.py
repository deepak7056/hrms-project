from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from tasks.models import DailyTaskReport, Task
import pandas as pd
import json
from datetime import datetime

@login_required
def upload_report(request):
    if request.user.role != 'admin':
        messages.error(request, 'Only admins can upload reports')
        return redirect('index')
    
    if request.method == 'POST' and request.FILES.get('excel_file'):
        try:
            excel_file = request.FILES['excel_file']
            
            # Delete previous reports
            DailyTaskReport.objects.all().delete()
            
            # Create new report
            report = DailyTaskReport.objects.create(
                uploaded_by=request.user,
                excel_file=excel_file
            )
            
            # Read Excel file
            df = pd.read_excel(excel_file)
            
            # Create tasks from each row
            for index, row in df.iterrows():
                # Convert row to dictionary, handling NaN values
                row_data = {}
                for col in df.columns:
                    value = row[col]
                    if pd.isna(value):
                        row_data[col] = None
                    elif isinstance(value, (int, float)):
                        row_data[col] = value
                    else:
                        row_data[col] = str(value)
                
                Task.objects.create(
                    report=report,
                    original_data=row_data
                )
            
            messages.success(request, f'Report uploaded successfully! {len(df)} tasks imported.')
            return redirect('today_reports')
            
        except Exception as e:
            messages.error(request, f'Error uploading file: {str(e)}')
    
    return render(request, 'upload_report.html')