from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Task, DailyTaskReport
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime



from django.http import JsonResponse
from datetime import datetime

@login_required
def today_reports(request):
    # Get the latest report
    latest_report = DailyTaskReport.objects.first()
    
    if latest_report:
        # Get all tasks EXCEPT those assigned to the current logged-in user
        all_tasks = Task.objects.filter(report=latest_report).exclude(assigned_to=request.user)
        
        # Extract column headers from the first task
        columns = []
        if all_tasks.exists():
            first_task = all_tasks.first()
            columns = list(first_task.original_data.keys())
    else:
        all_tasks = []
        columns = []
    
    context = {
        'user': request.user,
        'tasks': all_tasks,
        'columns': columns,
        'report': latest_report,
    }
    
    return render(request, 'today-reports.html', context)
@login_required
def start_task(request, task_id):
    if request.method == 'POST':
        try:
            task = Task.objects.get(id=task_id, assigned_to=request.user)
            task.status = 'in_progress'
            task.started_at = datetime.now()
            task.save()
            return JsonResponse({'success': True, 'message': 'Task started successfully!'})
        except Task.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Task not found'})
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@login_required
def end_task(request, task_id):
    if request.method == 'POST':
        try:
            task = Task.objects.get(id=task_id, assigned_to=request.user)
            task.status = 'completed'
            task.completed_at = datetime.now()
            task.save()
            return JsonResponse({'success': True, 'message': 'Task completed successfully!'})
        except Task.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Task not found'})
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@login_required
def start_all_tasks(request):
    if request.method == 'POST':
        tasks = Task.objects.filter(assigned_to=request.user, status='pending')
        count = tasks.update(status='in_progress', started_at=datetime.now())
        return JsonResponse({'success': True, 'message': f'{count} tasks started successfully!'})
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@login_required
def end_all_tasks(request):
    if request.method == 'POST':
        tasks = Task.objects.filter(assigned_to=request.user, status='in_progress')
        count = tasks.update(status='completed', completed_at=datetime.now())
        return JsonResponse({'success': True, 'message': f'{count} tasks completed successfully!'})
    return JsonResponse({'success': False, 'message': 'Invalid request'})

# Update analytics view to include status
# In tasks/views.py
@login_required
def analytics(request):
    # Get all tasks assigned to current user
    my_tasks = Task.objects.filter(assigned_to=request.user)
    
    task_list = []
    columns = []
    
    if my_tasks.exists():
        first_task = my_tasks.first()
        columns = list(first_task.original_data.keys())
        
        for task in my_tasks:
            task_data = {
                'id': task.id,
                'values': [task.original_data.get(col, '') for col in columns],
                'assigned_date': task.self_assigned_date.isoformat() if task.self_assigned_date else None,
                'excel_assigned': task.excel_assigned_to,  # Show who it was assigned to in Excel
                'status': task.status,
                'started_at': task.started_at.isoformat() if task.started_at else None,
                'completed_at': task.completed_at.isoformat() if task.completed_at else None,
                'is_self_assigned': bool(task.self_assigned_date)  # Flag to show if self-assigned
            }
            task_list.append(task_data)
    
    # Calculate stats
    stats = {
        'total': my_tasks.count(),
        'pending': my_tasks.filter(status='pending').count(),
        'in_progress': my_tasks.filter(status='in_progress').count(),
        'completed': my_tasks.filter(status='completed').count(),
        'excel_assigned': my_tasks.filter(self_assigned_date__isnull=True).count(),
        'self_assigned': my_tasks.filter(self_assigned_date__isnull=False).count()
    }
    
    context = {
        'user': request.user,
        'my_tasks': json.dumps(task_list),
        'columns': json.dumps(columns),
        'stats': json.dumps(stats),
    }
    
    return render(request, 'analytics-today-tasks.html', context)

@login_required
def self_assign_task(request, task_id):
    if request.method == 'POST':
        try:
            task = Task.objects.get(id=task_id)
            
            # Remove from previous owner and assign to current user
            task.assigned_to = request.user
            task.self_assigned_date = datetime.now()
            
            # Update the original_data to reflect new assignment
            if 'ASSIGN TO' in task.original_data:
                task.original_data['ASSIGN TO'] = request.user.username
            elif 'Assign To' in task.original_data:
                task.original_data['Assign To'] = request.user.username
            elif 'assign to' in task.original_data:
                task.original_data['assign to'] = request.user.username
            else:
                # Find the assign column name
                for key in task.original_data.keys():
                    if 'assign' in key.lower() and 'to' in key.lower():
                        task.original_data[key] = request.user.username
                        break
            
            task.save()
            
            return JsonResponse({
                'success': True, 
                'message': f'Task assigned to {request.user.username} successfully!'
            })
        except Task.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Task not found'})
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@login_required
def check_assignments(request):
    tasks = Task.objects.all().select_related('assigned_to')
    
    for task in tasks[:10]:  # Show first 10 tasks
        assign_to_value = task.original_data.get('ASSIGN TO', 'NOT FOUND')
        actual_assignment = task.assigned_to.username if task.assigned_to else 'NONE'
        print(f"Excel says: '{assign_to_value}' -> Actually assigned to: '{actual_assignment}'")
    
    return JsonResponse({'checked': True})