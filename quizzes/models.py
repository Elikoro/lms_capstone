from django.db import models
from accounts.models import User
from courses.models import Course

class Quiz(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name='quizzes')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"{self.course.title} - {self.title}"

class Question(models.Model):
    quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE,related_name='questions')
    text = models.CharField(max_length=500)
    def __str__(self): return self.text

class Option(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE,related_name='options')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    def __str__(self): return self.text

class Result(models.Model):
    quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE,related_name='results')
    student = models.ForeignKey(User,on_delete=models.CASCADE,related_name='quiz_results')
    score = models.IntegerField()
    submitted_at = models.DateTimeField(auto_now_add=True)
