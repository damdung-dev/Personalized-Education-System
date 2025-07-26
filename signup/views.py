from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse
import datetime
from .models import Student

def index(request):
    if request.method=="POST":
        if request.POST.get('register')=="create":
            gender=request.POST.get('gender')
            firstname=request.POST.get('first_name')
            lastname=request.POST.get('last_name')
            email=request.POST.get('email')
            password=request.POST.get('password')
            confirmPassword=request.POST.get('confirm-password')
            created_date=datetime.datetime.now()

            if password==confirmPassword:
                if gender=="Male":
                    Student.objects.create(
                    first_name=firstname,
                    last_name=lastname,
                    email=email,
                    password=password,
                    gender=1,
                    created_date=created_date,
                    )
                    return HttpResponse(firstname+','+lastname+','+email+','+password+','+gender)
                elif gender=="Female":
                    Student.objects.create(
                    first_name=firstname,
                    last_name=lastname,
                    email=email,
                    password=password,
                    gender=0,
                    created_date=created_date,
                    )
                    return HttpResponse(firstname+','+lastname+','+email+','+password+','+gender)
                else:
                    messages.error("Vui lòng chọn giới tính")
            else:
                messages.error(request,"mật khẩu không trùng khớp")
    return render(request,'signup/signup.html')