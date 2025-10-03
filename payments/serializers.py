from rest_framework import serializers
from .models import Payment, Enrollment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta: model = Payment; fields = '__all__'

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta: model = Enrollment; fields = '__all__'
