from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = 'accounts'
urlpatterns = [
    path('auth/', views.LoginOrRegisterView.as_view(), name='auth'),
    path('logout', views.logout_view, name='logout'),
    path('main-dashboard/', views.main_dashboard, name='main_dashboard')
]