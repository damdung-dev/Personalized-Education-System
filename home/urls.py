from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name='home'),
    path('account/', views.account_view,name='account'),
    path('courses/', views.courses_view,name='courses'),
    path('calendar/', views.calendar_view,name='calendar'),
    path('chat/', views.chat_view,name='chat'),
    path('notification/', views.notification_view,name='notifications'),
    path('results/', views.results_view,name='results'),
    path('documents/', views.documents_view,name='documents'),
    path('dashboard/', views.dashboard_view,name='dashboard'),
]