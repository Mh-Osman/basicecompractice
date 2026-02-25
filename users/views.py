from django.shortcuts import render

# Create your views here.
from rest_framework_simplejwt.tokens import RefreshToken,TokenError

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import Customer
from rest_framework.permissions import IsAuthenticated

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = Customer.objects.get(email=email)
        except Customer.DoesNotExist:
            return Response(
                {'error': 'User not found'}, 
                status=status.HTTP_404_NOT_FOUND
                )  
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'role': user.role,
                }
            })
        return Response(
            {'error': 'Invalid credentials'}, 
            status=status.HTTP_401_UNAUTHORIZED
            )

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        role = request.data.get('role')
        if not role:
            return Response(    
                {'error': 'Role is required'}, 
                status=status.HTTP_400_BAD_REQUEST
                )
        user = Customer.objects.create_user(email=email, password=password, role=role)
        user.is_active = True
        user.save()
        return Response({
            'message': 'User created successfully',
            'user': {
                'id': user.id,
                'email': user.email,
                'role': user.role,
            }
        })


class CreateStaffView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        role = request.data.get('role')
        if not role:
            return Response(
                {'error': 'Role is required'}, 
                status=status.HTTP_400_BAD_REQUEST
                )
        user = Customer.objects.create_user(email=email, password=password, role=role)
        user.is_active = True

        user.save()
        return Response({
            'message': 'User created successfully',
            'user': {
                'id': user.id,
                'email': user.email,
                'role': user.role,
            }
        })
