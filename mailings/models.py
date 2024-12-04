from django.db import models
from django.contrib.auth import get_user_model

class Client(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name or self.email


class Message(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()

    def __str__(self):
        return self.subject


class Mailing(models.Model):
    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('running', 'Запущена'),
        ('completed', 'Завершена'),
    ]
    
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='mailings')
    clients = models.ManyToManyField(Client, related_name='mailings')

    def __str__(self):
        return f"Рассылка: {self.message.subject} — {self.get_status_display()}"


class MailingAttempt(models.Model):
    STATUS_CHOICES = [
        ('success', 'Успешно'),
        ('failed', 'Не успешно'),
    ]
    
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='attempts')
    attempt_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    server_response = models.TextField()

    def __str__(self):
        return f"{self.mailing.message.subject} — {self.get_status_display()}"