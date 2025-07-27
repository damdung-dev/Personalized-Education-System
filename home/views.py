from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'home/home.html')

def account_view(request):
    return render(request,'home/account.html')

def calendar_view(request):
    return render(request,'home/calendar.html')

def chat_view(request):
    return render(request,'home/chat.html')

def courses_view(request):
    return render(request,'home/courses.html')

def documents_view(request):
    return render(request,'home/documents.html')

def notification_view(request):
    return render(request,'home/notification.html')

def results_view(request):
    return render(request,'home/results.html')

def dashboard_view(request):
    return render(request,'home/home.html')


