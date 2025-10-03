from django.db import models
from accounts.models import User
from courses.models import Course

class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollment_records')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollment_records')
    date_enrolled = models.DateTimeField(auto_now_add=True)
    progress = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.title}"
