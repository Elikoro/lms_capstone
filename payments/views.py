import requests
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Payment, Enrollment
from .serializers import PaymentSerializer, EnrollmentSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all(); serializer_class = PaymentSerializer; permission_classes = [IsAuthenticated]
    def perform_create(self, serializer): serializer.save(user=self.request.user)
    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        payment = self.get_object()
        url = f"https://api.paystack.co/transaction/verify/{payment.reference}"
        headers = {"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
        r = requests.get(url, headers=headers, timeout=10); data = r.json()
        if data.get('status') and data['data']['status']=='success':
            payment.status='success'; payment.save()
            Enrollment.objects.get_or_create(student=payment.user, course=payment.course)
            return Response({"detail":"Payment verified and enrolled"}, status=200)
        payment.status='failed'; payment.save()
        return Response({"detail":"Verification failed"}, status=400)
