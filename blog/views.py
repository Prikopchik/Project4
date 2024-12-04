from django.shortcuts import render
from .models import Post

def blog_stats(request):
    posts = Post.objects.order_by('-views_count')[:10] 
    return render(request, 'blog/blog_statistics.html', {'posts': posts})
