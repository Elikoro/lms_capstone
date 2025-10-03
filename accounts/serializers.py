from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,min_length=8)
    class Meta:
        model = User
        fields = ('id','username','email','password','first_name','last_name','role')
    def create(self, validated):
        pwd = validated.pop('password')
        user = User(**validated)
        user.set_password(pwd)
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','email','first_name','last_name','role','bio','avatar')
