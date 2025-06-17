from django.urls import path
from . import views

urlpatterns = [
    path('today/', views.today_reports, name='today_reports'),
    path('analytics/', views.analytics, name='analytics'),
    path('self-assign/<int:task_id>/', views.self_assign_task, name='self_assign_task'),
    path('start/<int:task_id>/', views.start_task, name='start_task'),
    path('end/<int:task_id>/', views.end_task, name='end_task'),
    path('start-all/', views.start_all_tasks, name='start_all_tasks'),
    path('end-all/', views.end_all_tasks, name='end_all_tasks'),
]