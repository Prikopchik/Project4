from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.contrib import messages
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
@permission_required('mailing.view_mailing', raise_exception=True)
def mailing_list(request):
    mailings = Mailing.objects.all()
    return render(request, 'mailing_list.html', {'mailings': mailings})


@login_required
def user_mailing_list(request):
    mailings = Mailing.objects.filter(user=request.user)
    return render(request, 'user_mailing_list.html', {'mailings': mailings})


@login_required
@permission_required('mailing.change_mailing', raise_exception=True)
def edit_mailing(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk, user=request.user)
    return render(request, 'edit_mailing.html', {'mailing': mailing})


@login_required
@permission_required('mailing.view_mailing', raise_exception=True)
def manager_mailing_list(request):
    mailings = Mailing.objects.all()
    return render(request, 'manager_mailing_list.html', {'mailings': mailings})

def get_mailing_list():
    mailings = cache.get('mailing_list')
    if not mailings:
        mailings = Mailing.objects.all()
        cache.set('mailing_list', mailings, 60 * 15)
    return mailings

@cache_control(public=True, max_age=86400)
def static_view(request):
    return render(request, 'static_page.html')