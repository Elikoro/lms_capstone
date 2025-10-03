from django.contrib import admin
from .models import Quiz, Question, Result

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'course')
    list_filter = ('course',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'quiz', 'text')
    list_filter = ('quiz',)

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ("id", "student", "quiz", "score", "submitted_at")
    list_filter = ("quiz", "submitted_at")
    search_fields = ("student__username", "quiz__title")
