import uuid
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import Group
from users.models import CustomUser
from .forms import CustomUserCreationForm, TokenConfirmationForm
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings
from .models import EmailConfirmationToken 
from .forms import CustomUserCreationForm
from django.db import transaction
from django.http import HttpResponse
from django.contrib.auth import get_user_model

User = get_user_model()
@transaction.atomic
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Создание пользователя
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()  # Сохраняем в БД

        # Проверяем, что пользователь действительно добавлен
        if not User.objects.filter(id=user.id).exists():
            print("Ошибка: пользователь не создан!")
            return render(request, 'registration.html', {'error': 'Ошибка регистрации, попробуйте снова.'})

        # Создание токена только если пользователь есть
        token = str(uuid.uuid4())
        EmailConfirmationToken.objects.create(user=user, token=token)
        print(token)
        return render(request, 'login.html')  # Перенаправляем на страницу входа

    return render(request, 'registration.html')

def confirm_email(request):
    if request.method == 'POST':
        form = TokenConfirmationForm(request.POST)
        if form.is_valid():
            token = form.cleaned_data['token']
            try:
                token_obj = EmailConfirmationToken.objects.get(token=token)
                user = token_obj.user
                user.is_active = True
                user.save()
                token_obj.delete() 
                return HttpResponse("Email подтвержден! Теперь вы можете войти.")
            except EmailConfirmationToken.DoesNotExist:
                return HttpResponse("Неверный или устаревший токен.")
    else:
        form = TokenConfirmationForm()
    return render(request, 'confirm_email.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('login')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('mailings:mailing_list')

def user_stats(request):
    users = CustomUser.objects.all()
    return render(request, 'user_statistics.html', {'users': users})

def email_confirmation_sent(request):
    return render(request, 'users/email_confirmation_sent.html')

