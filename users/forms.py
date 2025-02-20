from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

class TokenConfirmationForm(forms.Form):
    token = forms.CharField(max_length=32, label="Введите токен подтверждения")
