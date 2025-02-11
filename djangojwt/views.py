from django.shortcuts import render, redirect
from django.views import View
from .forms import CustomUserCreationForm
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import APIView
from django.contrib.auth.models import User
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from datetime import datetime, timedelta
from django.http import JsonResponse
import json

class Signup(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'djangojwt/signup.html', {'form': form})
        
    def post(self, request):
        try:
            data = json.loads(request.body)
            serializer = UserSerializer(data={
                'username': data.get('username'),
                'email': data.get('email'),
                'password': data.get('password')
            })
            
            if serializer.is_valid():
                user = serializer.save()
                refresh = RefreshToken.for_user(user)
                
                # Debug print
                print("Access Token:", str(refresh.access_token))
                print("Refresh Token:", str(refresh))
                
                response = JsonResponse({
                    'status': 'success',
                    'message': 'Signup successful'
                }, status=201)
                
                # Set tokens in HttpOnly cookies
                response.set_cookie(
                    'access_token',
                    str(refresh.access_token),
                    httponly=True,
                    samesite='Lax',
                    secure=True,
                    max_age=15 * 60
                )
                response.set_cookie(
                    'refresh_token',
                    str(refresh),
                    httponly=True,
                    samesite='Lax',
                    secure=True,
                    max_age=24 * 60 * 60
                )
                
                return response
            return JsonResponse(serializer.errors, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

class Login(View):
    def get(self, request):
        return render(request, 'djangojwt/login.html')  

    def post(self, request):
        try:
            print("=== Login attempt started ===")
            print("Request body:", request.body)
            
            data = json.loads(request.body)
            print("Parsed data:", data)
            
            username = data.get('username')
            password = data.get('password')
            
            print(f"Login attempt for user: {username}")
            
            user = authenticate(username=username, password=password)
            print(f"Authentication result: {'Success' if user else 'Failed'}")
            
            if user is None:
                print("Authentication failed - returning error response")
                return JsonResponse({
                    'error': 'Invalid credentials'
                }, status=400)

            login(request, user)
            print(f"Session login completed for user: {username}")
            
            refresh = RefreshToken.for_user(user)
            print("JWT tokens generated successfully")
            
            response = JsonResponse({
                'status': 'success',
                'message': 'Login successful'
            })
            
            print("Setting cookies...")
            # Set tokens in HttpOnly cookies
            response.set_cookie(
                'access_token',
                str(refresh.access_token),
                httponly=True,
                samesite='Lax',
                secure=True,  
                max_age=15 * 60  
            )
            response.set_cookie(
                'refresh_token',
                str(refresh),
                httponly=True,
                samesite='Lax',
                secure=True,  
                max_age=24 * 60 * 60  
            )
            
            print("=== Login completed successfully ===")
            return response
            
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {str(e)}")
            print("Raw request body:", request.body)
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            print(f"Unexpected error during login: {str(e)}")
            import traceback
            print("Traceback:", traceback.format_exc())
            return JsonResponse({'error': str(e)}, status=400)

class Logout(View):
    def post(self, request):
        response = JsonResponse({
            'status': 'success',
            'message': 'Logout successful'
        })
        
        # Delete the cookies
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        
        return response

class Home(LoginRequiredMixin,View):
    login_url = 'login'

    def get(self,request):
        return render(request,'djangojwt/home.html')


############ API ############

@permission_classes([IsAuthenticated])
class UserList(APIView):
    def get(self, request):
        users = User.objects.all()
        serializers = UserSerializer(users, many=True)
        return Response(serializers.data)
    
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([IsAuthenticated])
class UserDetail(APIView):
    
    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self,request,pk):
        user = User.objects.get(pk=pk)
        password = request.data.get('password')
        if password:
            request.data['password'] = make_password(password)
        serializer = UserSerializer(user,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request,pk):
        try:
            user = User.objects.get(pk=pk).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        
        
