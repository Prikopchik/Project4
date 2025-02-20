from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.contrib import messages

from mailings.forms import ClientForm, MailingForm, MessageForm
from .models import Mailing, MailingAttempt
from .utils import send_mailing 
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.cache import cache_page, cache_control
from django.core.cache import cache

class SendMailingView(View):
    def get(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        success = send_mailing(mailing) 
        if success:
            messages.success(request, "Рассылка успешно отправлена.")
        else:
            messages.error(request, "Не удалось отправить рассылку.")
        return redirect('mailing_detail', pk=pk) 

def mailing_stats(request):
    total_mailings = Mailing.objects.count()
    active_mailings = Mailing.objects.filter(status='Запущена').count()
    successful_attempts = MailingAttempt.objects.filter(status='Успешно').count()
    failed_attempts = MailingAttempt.objects.filter(status='Не успешно').count()

    context = {
        'total_mailings': total_mailings,
        'active_mailings': active_mailings,
        'successful_attempts': successful_attempts,
        'failed_attempts': failed_attempts,
    }
    return render(request, 'statistics.html', context)


@cache_page(60 * 15)
@login_required
@permission_required('mailings:view_mailing', raise_exception=True)
def mailing_list(request):
    mailings = Mailing.objects.all()
    return render(request, 'mailing_list.html', {'mailings': mailings})


@login_required
def mailing_list(request):
    mailings = Mailing.objects.filter(user=request.user)
    return render(request, 'mailing_list.html', {'mailings': mailings})


@login_required
def edit_mailing(request, mailing_id):
    """Редактирование существующей рассылки"""
    mailing = get_object_or_404(Mailing, id=mailing_id, user=request.user)

    if request.method == 'POST':
        form = MailingForm(request.POST, instance=mailing)
        if form.is_valid():
            form.save()
            return redirect('mailings:user_mailing_list')
    else:
        form = MailingForm(instance=mailing)

    return render(request, 'edit_mailing.html', {'form': form, 'mailing': mailing})



@login_required
@permission_required('mailing.view_mailing', raise_exception=True)
def user_mailing_list(request):
    mailings = Mailing.objects.all()
    return render(request, 'user_mailing_list.html', {'mailings': mailings})

def get_mailing_list():
    mailings = cache.get('mailing_list')
    if not mailings:
        mailings = Mailing.objects.all()
        cache.set('mailing_list', mailings, 60 * 15)
    return mailings

@cache_control(public=True, max_age=86400)
def static_view(request):
    return render(request, 'static_page.html')

def create_mailing(request):
    if request.method == 'POST':
        form = MailingForm(request.POST)
        if form.is_valid():
            mailing = form.save(commit=False)
            mailing.user = request.user  
            mailing.save()
            form.save_m2m()  
            return redirect('dashboard')  
    else:
        form = MailingForm()

    return render(request, 'create_mailing.html', {'form': form})


@login_required
def create_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mailings:create_mailing')  
    else:
        form = MessageForm()

    return render(request, 'create_message.html', {'form': form})


@login_required
def create_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mailings:create_mailing')  
    else:
        form = ClientForm()

    return render(request, 'create_client.html', {'form': form})


def view_mailing(request, mailing_id):
    """Просмотр одной рассылки"""
    mailing = get_object_or_404(Mailing, id=mailing_id)
    
    context = {
        'mailing': mailing
    }
    return render(request, 'view_mailing.html', context)



@login_required
def delete_mailing(request, mailing_id):
    """Удаление рассылки"""
    mailing = get_object_or_404(Mailing, id=mailing_id, user=request.user)

    if request.method == 'POST':
        mailing.delete()
        return redirect('mailings:user_mailing_list')

    return render(request, 'delete_mailing.html', {'mailing': mailing})
