from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User 
        fields = ['id', 'username', 'password', 'email']

class UserLoginSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User 
        fields = ['username', 'password']

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()