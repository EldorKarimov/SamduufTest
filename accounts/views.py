from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .models import *
from .forms import *

class SignUpView(View):
    def get(self, request):
        form = RegisterForm()
        pupil_form = PupilForm()
        context = {
            'form':form,
            'pupil_form':pupil_form
        }
        return render(request, 'accounts/register.html', context)
    def post(self, request):
        form = RegisterForm(request.POST)
        pupil_form = PupilForm(request.POST)
        
        context = {
            'form':form,
            'pupil_form':pupil_form
        }
        if form.is_valid() and pupil_form.is_valid():
            user_form = form.save()
            pupil_form = pupil_form.save(commit=False)
            pupil_form.user = user_form
            pupil_form.save()
            messages.success(request, "Siz muvaffaqqiyatli ro'yxatdan o'tdingiz")
            return redirect('quiz:home')
        else:
            return render(request, 'accounts/register.html', context)
        
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request=request, username=username, password=password)
        if user is not None:
            login(request=request, user=user)
            return redirect('quiz:home')
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('quiz:home')

def main_dashboard(request):
    return render(request, 'dashboards/main.html')