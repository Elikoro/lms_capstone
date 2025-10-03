from rest_framework import serializers
from .models import Quiz, Question, Option, Result

class OptionSerializer(serializers.ModelSerializer):
    class Meta: model = Option; fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)
    class Meta: model = Question; fields = ['id','quiz','text','options']

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    class Meta: model = Quiz; fields = ['id','course','title','description','created_at','questions']

class ResultSerializer(serializers.ModelSerializer):
    class Meta: model = Result; fields = '__all__'
