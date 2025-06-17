from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Leave, LeaveType
from accounts.models import User
import json
from datetime import datetime

@login_required
def leave_list(request):
    # Get user's leaves
    my_leaves = Leave.objects.filter(employee=request.user).order_by('-applied_date')
    
    # If manager, get team leaves for approval
    team_leaves = None
    if request.user.role in ['manager', 'admin']:
        if request.user.role == 'manager':
            # Get all employees who report to this manager
            team_employees = User.objects.filter(manager=request.user)
            team_leaves = Leave.objects.filter(
                employee__in=team_employees, 
                status='pending'
            ).select_related('employee', 'leave_type')
        else:  # admin
            team_leaves = Leave.objects.filter(status='pending').select_related('employee', 'leave_type')
    
    # Get leave types for the form
    leave_types = LeaveType.objects.all()
    
    context = {
        'user': request.user,
        'my_leaves': my_leaves,
        'team_leaves': team_leaves,
        'leave_types': leave_types,
    }
    return render(request, 'leave.html', context)

@login_required
def apply_leave(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            leave = Leave.objects.create(
                employee=request.user,
                leave_type_id=data['leave_type'],
                start_date=data['start_date'],
                end_date=data['end_date'],
                reason=data['reason']
            )
            return JsonResponse({'success': True, 'message': 'Leave applied successfully!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@login_required
def approve_leave(request, leave_id):
    if request.user.role not in ['manager', 'admin']:
        return JsonResponse({'success': False, 'message': 'Unauthorized'})
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            leave = Leave.objects.get(id=leave_id)
            
            # Check authorization
            if request.user.role == 'manager' and leave.employee.manager != request.user:
                return JsonResponse({'success': False, 'message': 'Unauthorized'})
            
            leave.status = data['status']  # 'approved' or 'rejected'
            leave.approved_by = request.user
            leave.approval_date = datetime.now()
            leave.comments = data.get('comments', '')
            leave.save()
            
            return JsonResponse({'success': True, 'message': f'Leave {leave.status} successfully!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Invalid request'})