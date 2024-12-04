from django.urls import path
from .views import SendMailingView

urlpatterns = [
    path('mailing/<int:pk>/send/', SendMailingView.as_view(), name='send_mailing'),
]
