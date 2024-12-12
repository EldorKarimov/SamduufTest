from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('register/', views.SignUpView.as_view(), name='register'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('main-dashboard/', views.main_dashboard, name='main_dashboard')
]