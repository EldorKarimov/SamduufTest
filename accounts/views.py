from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django import http
from django.db import transaction
from accounts.hemisAPI import HemisApi

from .models import *
from .forms import *

User = get_user_model()

class LoginOrRegisterView(View):
    def get(self, request):
        form = LoginOrRegisterForm()
        context = {
            'form':form
        }
        return render(request, 'accounts/auth.html', context)

    def post(self, request):
        form = LoginOrRegisterForm(request.POST)
        
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user_exists = User.objects.filter(username = username).exists()
            if user_exists:
                user = authenticate(request, username = username, password = password)
                if user is not None:
                    login(request, user)
                    return redirect('quiz:home')
                else:
                    return http.HttpResponse("Xatolik yuz berdi iltimos adminga xabar bering")
            else:
                student = self.create_student(username, password)
                login(request, student)
                return redirect('quiz:home')

        return render(request, 'accounts/auth.html', {'form':form})
    
    @transaction.atomic()
    def create_student(self, username, password):
        hemis_user_obj = HemisApi()
        hemis_user_data = hemis_user_obj.user_data_json(username, password)
        faculty, created = Faculty.objects.get_or_create(
            faculty_name = hemis_user_data.get('data').get('faculty').get('name')
        )
        specialty, created = Specialty.objects.get_or_create(
            specialty_name = hemis_user_data.get('data').get('specialty').get('name'),
            faculty = faculty
        )

        group, created = StudentGroup.objects.get_or_create(
            group_name = hemis_user_data.get('data').get('group').get('name'),
            specialty = specialty
        )
        
        user = User.objects.create(
            first_name = hemis_user_data.get('data').get('first_name'),
            last_name = hemis_user_data.get('data').get('second_name'),
            patronymic = hemis_user_data.get('data').get('third_name'),
            username = hemis_user_data.get('data').get('student_id_number'),
        )
        user.password = make_password(password)
        user.save()
        Student.objects.create(
            group = group,
            user = user
        )
        print("create student is working")
        return user


def logout_view(request):
    logout(request)
    return redirect('quiz:home')

def main_dashboard(request):
    return render(request, 'dashboards/main.html')