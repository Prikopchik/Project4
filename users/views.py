from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import Group
from users.models import CustomUser
from .forms import CustomUserCreationForm
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

@transaction.atomic
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            token = get_random_string(32)
            EmailConfirmationToken.objects.create(user=user, token=token)
            print(f"Токен создан: {token}")  # Отладочный вывод

            current_site = get_current_site(request)
            confirm_link = f"http://{current_site.domain}{reverse('users:confirm_email', args=[token])}"
            print(f"Ссылка для подтверждения: {confirm_link}")  # Отладочный вывод
            print(f"Токен создан: {token}")
            send_mail(
                'Подтверждение регистрации',
                f'Перейдите по ссылке для подтверждения: {confirm_link}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

            return redirect('email_confirmation_sent')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def user_stats(request):
    users = CustomUser.objects.all()
    return render(request, 'user_statistics.html', {'users': users})

def email_confirmation_sent(request):
    return render(request, 'users/email_confirmation_sent.html')

def confirm_email(request, token):
    try:
        token_obj = get_object_or_404(EmailConfirmationToken, token=token)
        user = token_obj.user
        user.is_active = True
        user.save()
        print(f"Пользователь {user.username} активирован: {user.is_active}")  
        token_obj.delete()
        return HttpResponse("Email подтвержден! Теперь вы можете войти.")
    except EmailConfirmationToken.DoesNotExist:
        return HttpResponse("Неверный или устаревший токен.")
