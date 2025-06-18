from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})

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

def initialize_admin(request):
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='Admin@123456'
        )
        return render(request, 'admin_created.html', {
            'message': 'Admin user created! Username: admin, Password: Admin@123456'
        })
    return redirect('login')