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

class Signup(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request,'djangojwt/signup.html',{'form':form})

    def post(self,request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('home')
        else:
            print(form.errors)

        return render(request,'djangojwt/signup.html',{'form':form})

class Login(View):
    def get(self,request):
        return render(request,'djangojwt/login.html')
    
    def post(self,request):
        username = request.POST['username']        
        password = request.POST['password1']

        user = authenticate(request, username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Invalid username or password')

        return render(request, 'djangojwt/login.html')
    
class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('login')


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
        
        
            