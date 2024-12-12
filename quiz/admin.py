from django.contrib import admin

from .models import *


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('title', 'duration', 'attempts_allowed', 'number_of_questions', 'is_available')
    list_editable = ('is_available', )
    search_fields = ('title', )
    list_filter = ('is_available', )

class AnswerInline(admin.TabularInline):
    model = Answer
    fields = ('name', 'is_correct')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'is_multiple_choice')

    inlines = [AnswerInline]



admin.site.register([UserAttempt, UserAnswer, Science])