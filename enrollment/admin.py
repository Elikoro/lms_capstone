from django.contrib import admin
from .models import Enrollment

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'course', 'date_enrolled', 'progress')
    list_filter = ('date_enrolled', 'course')
    search_fields = ('user__username', 'course__title')
