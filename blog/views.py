from django.shortcuts import render
from .models import BlogPost

def blog_stats(request):
    posts = BlogPost.objects.order_by('-views_count')[:10] 
    return render(request, 'blog_statistics.html', {'posts': posts})
