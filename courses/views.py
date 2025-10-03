from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Course, Module, Lesson, LessonProgress
from .serializers import CourseSerializer, ModuleSerializer, LessonSerializer
from .permissions import IsInstructorOrAdmin
from rest_framework.decorators import action
from rest_framework.response import Response
from payments.models import Enrollment
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Course
from enrollment.models import Enrollment

# List all courses
def course_list(request):
    courses = Course.objects.all()
    return render(request, "courses/course_list.html", {"courses": courses})

# Course detail + enroll button
@login_required
def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)

    # check if user already enrolled
    enrolled = Enrollment.objects.filter(user=request.user, course=course).exists()

    if request.method == "POST" and not enrolled:
        Enrollment.objects.create(user=request.user, course=course)
        return redirect("course_detail", pk=course.pk)

    return render(request, "courses/course_detail.html", {"course": course, "enrolled": enrolled})


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    def get_permissions(self):
        if self.action in ['create','update','partial_update','destroy']:
            return [IsAuthenticated(), IsInstructorOrAdmin()]
        return [AllowAny()]
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def enroll(self, request, pk=None):
        course = self.get_object()
        user = request.user
        if Enrollment.objects.filter(student=user, course=course).exists():
            return Response({"detail":"Already enrolled"}, status=400)
        if course.price and course.price > 0:
            return Response({"detail":"Course requires payment. Call payments API."}, status=402)
        Enrollment.objects.create(student=user, course=course)
        return Response({"detail":"Enrolled"}, status=201)
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def progress(self, request, pk=None):
        course = self.get_object()
        total = Lesson.objects.filter(module__course=course).count()
        if total==0: return Response({"progress":0})
        done = LessonProgress.objects.filter(student=request.user, lesson__module__course=course, completed=True).count()
        percent = round((done/total)*100,2)
        return Response({"progress":percent,"completed":done,"total":total})

class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    def get_permissions(self):
        if self.action in ['create','update','partial_update','destroy']:
            return [IsAuthenticated(), IsInstructorOrAdmin()]
        return [IsAuthenticated()]

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    def get_permissions(self):
        if self.action in ['create','update','partial_update','destroy']:
            return [IsAuthenticated(), IsInstructorOrAdmin()]
        return [IsAuthenticated()]
    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.is_authenticated and user.role in ('instructor','admin'):
            return qs
        enrolled_courses = Enrollment.objects.filter(student=user).values_list('course_id',flat=True)
        return qs.filter(module__course_id__in=enrolled_courses)
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def complete(self, request, pk=None):
        lesson = self.get_object()
        user = request.user
        if not Enrollment.objects.filter(student=user, course=lesson.module.course).exists() and user.role not in ('admin','instructor'):
            return Response({"detail":"Not enrolled"}, status=403)
        lp, created = LessonProgress.objects.get_or_create(student=user, lesson=lesson)
        if not lp.completed:
            from django.utils import timezone
            lp.completed = True
            lp.completed_at = timezone.now()
            lp.save()
        total = Lesson.objects.filter(module__course=lesson.module.course).count()
        done = LessonProgress.objects.filter(student=user, lesson__module__course=lesson.module.course, completed=True).count()
        percent = round((done/total)*100,2) if total else 0
        return Response({"detail":"Marked","progress":percent})
