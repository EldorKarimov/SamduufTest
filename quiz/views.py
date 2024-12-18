from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django import http
from django.utils import timezone
from django.contrib import messages
from django.db import transaction

from .forms import QuestionsAddForm
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
        try:
            with transaction.atomic():
                score = 0
                correct_answers_count = 0
                for question in Question.objects.filter(test = test):
                    selected_answer_id = request.POST.get(str(question.id))
                    if selected_answer_id:
                        selected_answer = Answer.objects.get(id = selected_answer_id)
                        print(selected_answer.name)
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
        except Exception as e:
            return http.HttpResponse(f"Xatolik yuz berdi. {e}")

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
        

class TestListView(LoginRequiredMixin, View):
    def get(self, request):
        tests = Test.objects.all()
        context = {
            'tests':tests
        }
        return render(request, 'quiz/test-list.html', context)

class QuestionAddView(LoginRequiredMixin, View):
    def get(self, request, test_id):
        test = get_object_or_404(Test, id = test_id)
        form = QuestionsAddForm()
        return render(request, 'quiz/add-questions.html', {'form':form})
    def post(self, request, test_id):
        test = get_object_or_404(Test, id = test_id)
        form = QuestionsAddForm(request.POST)
        if form.is_valid():
            questions_data = form.cleaned_data['questions']
            try:
                questions_answers = questions_data.strip().split('===')
                
                for block in questions_answers:  
                    lines = block.strip().split("\n")
                    question_text = lines[0].lstrip('#') 
                    
                    question = Question.objects.create(
                        test = test,
                        name = question_text
                    )
                    
                    for line in lines[1:]:
                        is_correct = line.startswith("+")  
                        answer_text = line[1:].strip() 
                        Answer.objects.create(
                            question = question, 
                            name = answer_text,
                            is_correct = is_correct
                        )

                messages.success(request, "Savollar muvaffaqiyatli qo'shildi!")
                return http.HttpResponse("welcome")
            except Exception as e:
                messages.error(request, f"Xato yuz berdi: {e}")