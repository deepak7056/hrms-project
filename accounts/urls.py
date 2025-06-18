from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from accounts.views import initialize_admin

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.profile_view, name='profile'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('logout/', views.logout_view, name='logout'),  # Changed to custom view
    path('init-admin/', initialize_admin, name='init_admin'),
]