from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from django.contrib.sessions.middleware import SessionMiddleware
from django.utils.timezone import now
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib import auth
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.utils.decorators import method_decorator

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema
from .serializer import ForgotPasswordSerializer, UserLoginSerializer, UserSerializer
from drf_spectacular.utils import extend_schema
from drf_spectacular.openapi import OpenApiParameter, OpenApiExample, OpenApiTypes

# Add password validatiion check regex's
# Add email check

@extend_schema(
    request=UserSerializer,
    responses=UserSerializer,
    description="User Registration"
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        return Response({'user':serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    request=UserLoginSerializer,
    responses={},
    description="User Login"
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])
    user = auth.authenticate(username=request.data['username'], password=request.data['password'])
    # if not user.check_password(request.data['password']):
    #     return Response('User is not registered', status=status.HTTP_404_NOT_FOUND)
    if user is not None:
        auth.login(request=request, user=user)
        serializer = UserSerializer(user)
        return Response("Success", status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@extend_schema(
    request=ForgotPasswordSerializer,
    responses={},
    description="Forgot Password"
)
@api_view(['POST'])
@permission_classes([AllowAny])
def forgotpassword(request):
    user = get_object_or_404(User, email=request.data['email'])
    serializer = UserSerializer(user)
    return Response("Password reset email sent.", status=status.HTTP_200_OK)

@extend_schema(
    request={},
    responses={},
    description="User Logout"
)
@api_view(['GET'])
def logout(request):
    auth.logout(request=request)
    return Response("User logged out.", status=status.HTTP_200_OK)
