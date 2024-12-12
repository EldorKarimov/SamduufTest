from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django import http
from django.utils import timezone
from django.contrib import messages

from .models import *

class HomePageView(View):
    def get(self, request):
        tests = Test.objects.filter(is_available = True)
        context = {
            'tests':tests
        }
        return render(request, 'index.html', context)
    
class TestDetailView(LoginRequiredMixin, View):
    def get(self, request, test_id):
        test = get_object_or_404(Test, id = test_id)
        context = {
            'test':test
        }
        return render(request, 'quiz/test-detail.html', context)
    
class TestPageView(LoginRequiredMixin, View):
    def get(self, request, test_id):
        test = get_object_or_404(Test, id = test_id)

        attempt_count = UserAttempt.objects.filter(user = request.user, test = test).count()
        if attempt_count >= test.attempts_allowed:
            messages.error(request, f"Testga {test.attempts_allowed} marta urinish berilgan sizning urinishingiz tugadi.")
            return redirect('quiz:test_detail', test.id)
        
        context = {
            'test':test
        }
        UserAttempt.objects.create(
            user = request.user,
            test = test,
            score = 0,
            time_taken = timezone.timedelta(0),
        )
        return render(request, 'quiz/test-page.html', context)
    
    def post(self, request, test_id):
        test = get_object_or_404(Test, id = test_id)
        attempt = UserAttempt.objects.filter(user = request.user, test = test).last()
        if attempt.is_completed:
            return http.HttpResponse("Siz allaqachon testni tugatgansiz")
        score = 0
        correct_answers_count = 0
        for question in test.get_questions:
            selected_answer_id = request.POST.get(str(question.id))
            if selected_answer_id:
                selected_answer = Answer.objects.get(id = selected_answer_id)
                user_answer = UserAnswer.objects.create(
                    attempt = attempt,
                    question = question,
                    selected_answer = selected_answer,
                    is_correct = selected_answer.is_correct
                )
                user_answer.save()
                if selected_answer.is_correct:
                    score += question.mark
                    correct_answers_count += 1
        attempt.score = score
        attempt.time_taken = timezone.now() - attempt.created
        attempt.is_completed = True
        attempt.save()

        context = {
            "test":test,
            "attempt":attempt,
            "correct_answers_count":correct_answers_count
        }
            
        return redirect('quiz:result_detail', attempt.id)
    
class ResultsListView(LoginRequiredMixin, View):
    def get(self, request):
        attempts = UserAttempt.objects.all()
        user_answers = UserAnswer.objects.all()
        context = {
            "attempts":attempts,
            "user_answers":user_answers
        }
        return render(request, 'quiz/results.html', context)

class ResultDetailView(LoginRequiredMixin, View):
    def get(self, request, attempt_id):
        attempt = get_object_or_404(UserAttempt, id = attempt_id)
        user_answers = UserAnswer.objects.filter(attempt = attempt)
        context = {
            'user_answers':user_answers,
            'attempt':attempt
        }
        return render(request, "quiz/result-detail.html", context)
        