from django.urls import path
from . import views

urlpatterns = [
    path('', views.leave_list, name='leave_list'),
    path('apply/', views.apply_leave, name='apply_leave'),
    path('approve/<int:leave_id>/', views.approve_leave, name='approve_leave'),
]