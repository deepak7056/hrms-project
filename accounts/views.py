from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User

@login_required
def index(request):
    all_users = User.objects.all().select_related('manager')
    
    # Get users by role
    admins = all_users.filter(role='admin')
    managers = all_users.filter(role='manager')
    employees = all_users.filter(role='employee')
    
    # Get specific managers by name (more reliable than employee_id)
    anupam = User.objects.filter(
        first_name='Anupam', 
        last_name='Mishra',
        role='manager'
    ).first()
    
    sourabh = User.objects.filter(
        first_name='Sourabh', 
        last_name='Lochave',
        role='manager'
    ).first()
    
    # Create department-based hierarchy
    # Explicitly assign Sourabh to both Analytics and Order Management
    department_hierarchy = {
        'PDM': {
            'manager': anupam,
            'employees': employees.filter(department='PDM')
        },
        'Analytics': {
            'manager': sourabh,  # Sourabh manages Analytics
            'employees': employees.filter(department='Analytics')
        },
        'Order_Management': {
            'manager': sourabh,  # Same Sourabh manages Order Management
            'employees': employees.filter(department='Order Management')
        }
    }
    
    context = {
        'user': request.user,
        'admins': admins,
        'managers': managers,
        'all_users': all_users,
        'department_hierarchy': department_hierarchy,
    }
    
    return render(request, 'index.html', context)
def login_view(request):
    # Your existing login code
    if request.user.is_authenticated:
        return redirect('index')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid Username or Password')
            
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')  # This is the correct simple logout