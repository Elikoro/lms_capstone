from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Quiz, Question, Result, Option
from .serializers import QuizSerializer, ResultSerializer
from courses.permissions import IsInstructorOrAdmin

class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    def get_permissions(self):
        if self.action in ['create','update','destroy']:
            return [IsAuthenticated(), IsInstructorOrAdmin()]
        return [IsAuthenticated()]
    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        quiz = self.get_object()
        answers = request.data.get('answers',{})  # {question_id: option_id}
        score = 0
        for qid, oid in answers.items():
            try:
                q = Question.objects.get(id=int(qid), quiz=quiz)
                if q.options.filter(id=int(oid), is_correct=True).exists():
                    score += 1
            except Question.DoesNotExist:
                continue
        res = Result.objects.create(quiz=quiz, student=request.user, score=score)
        return Response(ResultSerializer(res).data, status=201)
