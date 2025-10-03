from django.db import models
from accounts.models import User
from courses.models import Course

class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='payment_enrollments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('pending','Pending'),('success','Success'),('failed','Failed')])
    reference = models.CharField(max_length=100, unique=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} paid for {self.course.title}"


class Payment(models.Model):
    STATUS = (('pending','Pending'),('success','Success'),('failed','Failed'))
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='payments')
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name='payments')
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    reference = models.CharField(max_length=200, unique=True)
    status = models.CharField(max_length=10, choices=STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
