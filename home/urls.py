from django.urls import path
from . import views,views_chat
from django.conf import settings
from django.conf.urls.static import static

app_name = 'home'

urlpatterns = [
    path('', views.index,name='home'),
    path('account/', views.account_view,name='account'),
    path('courses/', views.courses_view,name='courses'),
    path('calendar/', views.calendar_view,name='calendar'),
    path('chat/', views_chat.chat_page,name='chat'),
    path('notification/', views.notification_view,name='notifications'),
    path('results/', views.results_view,name='results'),
    path('documents/', views.documents_view,name='documents'),
    path('dashboard/', views.dashboard_view,name='dashboard'),
    path('report/', views.report, name='report'),
    path('teachers/', views.teachers, name='teachers'),
    path('centers/', views.centers, name='centers'),
    path('help/', views.help_page, name='help'),
    path('login/', views.login_view, name='exit'),
    path('register-course/<str:code>/', views.register_course, name='register_course'),
    path('course-detail/<str:code>/', views.course_detail, name='course_detail'),
    path('chat/api/', views_chat.chat_api, name='chat_api'),

    
]