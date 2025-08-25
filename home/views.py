from django.shortcuts import render, redirect
from .models import StudentsAccount, RecommendDocument, CourseModule,RecommendCourse, ListLesson, Teacher
from signup.models import Student
from .forms import DocumentUploadForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime
from datetime import datetime
import calendar

def index(request):
    # Lấy email từ session
    email = request.session.get('user_email')
    if not email:
        return redirect('login')

    # Lấy thông tin user
    try:
        user = StudentsAccount.objects.get(email=email)
        approved = True
    except StudentsAccount.DoesNotExist:
        try:
            user = Student.objects.get(email=email)
            approved = False
        except Student.DoesNotExist:
            return redirect('login')

    # Lấy các thống kê
    mycourse = RecommendCourse.objects.filter(student=user)

    ongoing_courses = mycourse.filter(student=user, status="studying").count()
    completed_courses = mycourse.filter(status="passed").count()
    documents_count = RecommendDocument.objects.count()

    total_courses = mycourse.count()
    avg_progress = round((completed_courses / total_courses) * 100, 2) if total_courses > 0 else 0

    # Truyền dữ liệu sang template
    return render(request, 'home/home.html', {
        "user": user,
        "approved": approved,
        "ongoing_courses": ongoing_courses,
        "completed_courses": completed_courses,
        "documents_count": documents_count,
        "avg_progress": avg_progress,
    })

def account_view(request):
    email = request.session.get('user_email')

    if not email:
        return redirect('login')

    try:
        user = StudentsAccount.objects.get(email=email)
        approved = True
    except StudentsAccount.DoesNotExist:
        try:
            user = Student.objects.get(email=email)
            approved = False
        except Student.DoesNotExist:
            return redirect('login')

    return render(request, 'home/account.html', {
        'user': user,
        'approved': approved
    })

def calendar_view(request):
    today = datetime.today()
    year = today.year
    month = today.month

    cal = calendar.Calendar(firstweekday=0)
    month_days = [day for day in cal.itermonthdates(year, month)]

    weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    context = {
        'year': year,
        'month': month,
        'today': today,
        'month_days': month_days,
        'weekdays': weekdays,
    }
    return render(request, 'home/calendar.html', context)

def courses_view(request):
    email = request.session.get('user_email')
    if not email:
        return redirect('login')

    student = StudentsAccount.objects.get(email=email)

    # Khóa học đã đăng ký
    my_courses = RecommendCourse.objects.filter(student=student)

    # Khóa học hiện có (Course) mà sinh viên chưa đăng ký
    registered_codes = my_courses.values_list('code', flat=True)
    suggested_courses = CourseModule.objects.exclude(code__in=registered_codes)

    return render(request, 'home/courses.html', {
        'my_courses': my_courses,
        'suggested_courses': suggested_courses
    })

def documents_view(request):
    my_docs = 0
    recommend_books = RecommendDocument.objects.all()

    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home:documents')
    else:
        form = DocumentUploadForm()

    return render(request, 'home/documents.html', {
        'my_documents': my_docs,
        'my_documents_count': 0,
        'recommend_books': recommend_books,
        'recommend_count': recommend_books.count(),
        'form': form
    })

def register_course(request, code):
    course = get_object_or_404(CourseModule, code=code)
    # tạo RecommendCourse với code, name, credits ...

    # Lấy email từ session
    email = request.session.get('user_email')
    if not email:
        return JsonResponse({"success": False, "message": "Chưa đăng nhập hoặc session hết hạn"}, status=400)

    try:
        student = StudentsAccount.objects.get(email=email)
    except StudentsAccount.DoesNotExist:
        return JsonResponse({"success": False, "message": f"Không tìm thấy sinh viên với email {email}"}, status=400)

    try:
        course = CourseModule.objects.get(code=code)
    except CourseModule.DoesNotExist:
        return JsonResponse({"success": False, "message": "Không tìm thấy khóa học!"}, status=400)

    # Kiểm tra xem đã đăng ký chưa
    if RecommendCourse.objects.filter(student=student, code=course.code).exists():
        return JsonResponse({"success": False, "message": "Bạn đã đăng ký khóa học này!"})

    # Tạo bản ghi mới trong MyCourse
    RecommendCourse.objects.create(
        student=student,
        code=course.code,
        name=course.name,
        credits=course.credits,
        status='Studying'
    )

    return JsonResponse({"success": True, "message": "Đăng ký thành công!"})

def course_detail(request, code):
    # Lấy khóa học đã đăng ký của sinh viên
    email = request.session.get('user_email')
    mycourse = get_object_or_404(RecommendCourse, code=code, student__email=email)

    # Lấy CourseModule gốc
    course_module = get_object_or_404(CourseModule, code=mycourse.code)

    # Lấy tất cả bài học
    lessons = ListLesson.objects.filter(course=course_module)

    return render(request, 'home/course_detail.html', {
        'course': mycourse,
        'lessons': lessons,
    })


def notification_view(request):
    return render(request, 'home/notification.html')

def results_view(request):
    email = request.session.get('user_email')
    if not email:
        return redirect('login')

    student = StudentsAccount.objects.get(email=email)
    # Lấy toàn bộ dữ liệu RecommendCourse
    my_courses = RecommendCourse.objects.filter(student=student)

    # Truyền sang template
    return render(request, 'home/results.html', {'recommend_courses': my_courses})

def dashboard_view(request):
    # Lấy email từ session
    email = request.session.get('user_email')
    if not email:
        return redirect('login')

    # Lấy thông tin user
    try:
        user = StudentsAccount.objects.get(email=email)
        approved = True
    except StudentsAccount.DoesNotExist:
        try:
            user = Student.objects.get(email=email)
            approved = False
        except Student.DoesNotExist:
            return redirect('login')

    # Lấy các thống kê
    mycourse = RecommendCourse.objects.filter(student=user)

    ongoing_courses = mycourse.filter(status="studying").count()
    completed_courses = mycourse.filter(status="passed").count()
    documents_count = RecommendDocument.objects.count()

    total_courses = mycourse.count()
    avg_progress = round((completed_courses / total_courses) * 100, 2) if total_courses > 0 else 0

    # Truyền dữ liệu sang template
    return render(request, 'home/home.html', {
        "user": user,
        "approved": approved,
        "ongoing_courses": ongoing_courses,
        "completed_courses": completed_courses,
        "documents_count": documents_count,
        "avg_progress": avg_progress,
    })

def report(request):
    return render(request, 'home/report.html')

def teachers(request):
    teachers = Teacher.objects.all()
    return render(request, "home/teachers.html", {"teachers": teachers})

def centers(request):
    email = request.session.get('user_email')
    if not email:
        return redirect('login')

    student = StudentsAccount.objects.get(email=email)

    # Khóa học đã đăng ký
    my_courses = RecommendCourse.objects.filter(student=student)

    # Khóa học hiện có (Course) mà sinh viên chưa đăng ký
    registered_codes = my_courses.values_list('code', flat=True)
    suggested_courses = CourseModule.objects.exclude(code__in=registered_codes)

    return render(request, 'home/centers.html', {
        'my_courses': my_courses,
        'suggested_courses': suggested_courses
    })

def help_page(request):
    return render(request, 'home/help.html')

def login_view(request):
    return render(request, "login/login.html")
