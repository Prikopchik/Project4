from django.db import models
from django.conf import settings

class BlogPost(models.Model):
    STATUS_CHOICES = [
        ('Опубликована', 'Опубликована'),
        ('Черновик', 'Черновик'),
    ]
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views_count = models.PositiveIntegerField(default=0)
    published_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Черновик')

    def __str__(self):
        return self.title
