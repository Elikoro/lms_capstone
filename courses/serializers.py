from rest_framework import serializers
from .models import Course, Module, Lesson, LessonProgress, Category, Tag

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

class ModuleSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    class Meta:
        model = Module
        fields = ['id','course','title','description','order','lessons']

class CourseSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True, read_only=True)
    enrolled_count = serializers.SerializerMethodField()
    class Meta:
        model = Course
        fields = ['id','title','slug','description','category','tags','price','instructor','status','published_at','created_at','modules','enrolled_count']
    def validate_title(self,value):
        if not value.strip(): raise serializers.ValidationError("Title cannot be empty")
        return value
    def validate_description(self,value):
        if not value.strip(): raise serializers.ValidationError("Description cannot be empty")
        return value
    def get_enrolled_count(self,obj):
        try:
            from payments.models import Enrollment
            return Enrollment.objects.filter(course=obj).count()
        except Exception:
            return 0
