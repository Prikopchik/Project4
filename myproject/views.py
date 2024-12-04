from django.shortcuts import render
from mailings.models import Mailing, Recipient
from users.models import CustomUser
from blog.models import BlogPost
from django.views.decorators.cache import cache_page

def dashboard(request):
    total_mailings = Mailing.objects.count()
    active_mailings = Mailing.objects.filter(status='Запущена').count()
    unique_recipients = Recipient.objects.distinct().count()
    
    total_users = CustomUser.objects.count()
    active_users = CustomUser.objects.filter(is_active=True).count()
    blocked_users = CustomUser.objects.filter(is_blocked=True).count()
    
    total_posts = BlogPost.objects.filter(status='Опубликована').count()
    popular_posts = BlogPost.objects.order_by('-views')[:5]  
    
    context = {
        'total_mailings': total_mailings,
        'active_mailings': active_mailings,
        'unique_recipients': unique_recipients,
        'total_users': total_users,
        'active_users': active_users,
        'blocked_users': blocked_users,
        'total_posts': total_posts,
        'popular_posts': popular_posts,
    }
    
    return render(request, 'main/dashboard.html', context)


@cache_page(60 * 60) 
def main_page(request):
    active_mailings = Mailing.objects.filter(status='Запущена')
    completed_mailings = Mailing.objects.filter(status='Завершена')
    total_mailings = Mailing.objects.count()
    return render(request, 'main.html', {
        'active_mailings': active_mailings,
        'completed_mailings': completed_mailings,
        'total_mailings': total_mailings
    })