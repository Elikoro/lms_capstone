from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views 
from .views import CourseViewSet, ModuleViewSet, LessonViewSet

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'modules', ModuleViewSet, basename='module')
router.register(r'lessons', LessonViewSet, basename='lesson')

urlpatterns = [path('', include(router.urls)),
path("", views.course_list, name="course_list"),

path("<int:pk>/", views.course_detail, name="course_detail"),

]
