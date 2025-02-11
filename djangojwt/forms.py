from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'username','name':'username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control','id':'email','name':'email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','id':'password','name':'password1'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','id':'password','name':'password2'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1','password2']