from django.urls import path
from mailings import views

app_name = 'mailings'

urlpatterns = [
    path('<int:pk>/send/', views.SendMailingView.as_view(), name='send_mailing'),
    path('statistics/', views.mailing_stats, name='statistics'),
    path('mailing_list/', views.mailing_list, name='mailing_list'),
    path('user_mailing_list/', views.user_mailing_list, name='user_mailing_list'),
    path('edit_mailing/', views.edit_mailing, name='edit_mailing'),
    path('manager_mailing_list/', views.manager_mailing_list, name='manager_mailing_list'),
    path('static_page/', views.static_view, name='static_page'),
    
    ]
