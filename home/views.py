from django.shortcuts import render, redirect
from .models import StudentsAccount, RecommendDocument, CourseModule,RecommendCourse, ListLesson, Teacher, UserAction, ListLesson
from signup.models import Student
from .forms import DocumentUploadForm
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from llama_cpp import Llama
from datetime import datetime
import calendar
from django.utils.timezone import make_naive
from django.db.models import Count
from django.db.models.functions import TruncDate
import json

def index(request):
    email = request.session.get('user_email')
    if not email:
        return redirect('login')

    try:
        student_acc = StudentsAccount.objects.get(email=email)
    except StudentsAccount.DoesNotExist:
        return redirect('login')
    
    auth_user = student_acc

    # Khởi tạo list sessions
    watch_sessions = []
    start_time = None

    # Lấy toàn bộ UserAction theo thời gian
    actions = UserAction.objects.filter(user=auth_user).order_by("timestamp")

    # Duyệt qua hành động để tính duration
    for action in actions:
        if action.action == "play":
            start_time = action.timestamp
        elif action.action in ["pause", "done", "back"] and start_time:
            end_time = action.timestamp
            duration = (end_time - start_time).total_seconds()
            watch_sessions.append({
                "date": make_naive(end_time).date().strftime("%Y-%m-%d"),
                "duration": duration
            })
            start_time = None

    # Gộp thời gian theo ngày
    daily_duration = {}
    for session in watch_sessions:
        d = session["date"]
        daily_duration[d] = daily_duration.get(d, 0) + session["duration"]

    # Chuẩn bị dữ liệu cho chart
    action_dates = list(daily_duration.keys())
    action_durations = list(daily_duration.values())

    # Các thống kê khác
    mycourse = RecommendCourse.objects.filter(student_id=student_acc.student_id) 
    ongoing_courses = mycourse.filter(status="studying").count() 
    completed_courses = mycourse.filter(status="passed").count() 
    documents_count = RecommendDocument.objects.count() 
    total_courses = mycourse.count()
    avg_progress = round((completed_courses / total_courses) * 100, 2) if total_courses else 0

    return render(request, "home/home.html", {
        "user": student_acc,
        "action_dates": json.dumps(action_dates),
        "action_counts": json.dumps(action_durations),
        "ongoing_courses": ongoing_courses,
        "completed_courses": completed_courses, 
        "documents_count": documents_count, 
        "avg_progress": avg_progress, 
    })


def dashboard_view(request):
    email = request.session.get('user_email')
    if not email:
        return redirect('login')

    try:
        student_acc = StudentsAccount.objects.get(email=email)
    except StudentsAccount.DoesNotExist:
        return redirect('login')
    
    auth_user = student_acc

    # Khởi tạo list sessions
    watch_sessions = []
    start_time = None

    # Lấy toàn bộ UserAction theo thời gian
    actions = UserAction.objects.filter(user=auth_user).order_by("timestamp")

    # Duyệt qua hành động để tính duration
    for action in actions:
        if action.action == "play":
            start_time = action.timestamp
        elif action.action in ["pause", "done", "back"] and start_time:
            end_time = action.timestamp
            duration = (end_time - start_time).total_seconds()
            watch_sessions.append({
                "date": make_naive(end_time).date().strftime("%Y-%m-%d"),
                "duration": duration
            })
            start_time = None

    # Gộp thời gian theo ngày
    daily_duration = {}
    for session in watch_sessions:
        d = session["date"]
        daily_duration[d] = daily_duration.get(d, 0) + session["duration"]

    # Chuẩn bị dữ liệu cho chart
    action_dates = list(daily_duration.keys())
    action_durations = list(daily_duration.values())

    # Các thống kê khác
    mycourse = RecommendCourse.objects.filter(student_id=student_acc.student_id) 
    ongoing_courses = mycourse.filter(status="studying").count() 
    completed_courses = mycourse.filter(status="passed").count() 
    documents_count = RecommendDocument.objects.count() 
    total_courses = mycourse.count()
    avg_progress = round((completed_courses / total_courses) * 100, 2) if total_courses else 0

    return render(request, "home/home.html", {
        "user": student_acc,
        "action_dates": json.dumps(action_dates),
        "action_counts": json.dumps(action_durations),
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
    my_courses = RecommendCourse.objects.filter(student_id=student.student_id)

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
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Phương thức không hợp lệ"})

    email = request.session.get('user_email')
    if not email:
        return JsonResponse({"success": False, "message": "Chưa đăng nhập"})

    student = get_object_or_404(StudentsAccount, email=email)
    course = get_object_or_404(CourseModule, code=code)

    # Kiểm tra đã đăng ký
    if RecommendCourse.objects.filter(student_id=student.student_id, code=course.code).exists():
        return JsonResponse({"success": False, "message": "Bạn đã đăng ký khóa học này!"})

    # Tạo bản ghi mới
    RecommendCourse.objects.create(
        student_id=student.student_id,  # dùng student_id kiểu varchar
        code=course.code,
        name=course.name,
        credits=course.credits,
        status='studying'
    )

    return JsonResponse({"success": True, "message": "Đăng ký thành công!"})

def course_detail(request, code):
    # Lấy email từ session
    email = request.session.get('user_email')
    if not email:
        return redirect('login')

    # Lấy thông tin student
    student = get_object_or_404(StudentsAccount, email=email)

    # Lấy khóa học
    course_module = get_object_or_404(CourseModule, code=code)

    # Lấy các bài học trong khóa học
    lessons = ListLesson.objects.filter(course=course_module)

    # Kiểm tra xem student đã đăng ký khóa học chưa
    registered = RecommendCourse.objects.filter(student_id=student.student_id, code=course_module.code).exists()

    return render(request, 'home/course_detail.html', {
        'course': course_module,
        'lessons': lessons,
        'registered': registered,
        'student': student
    })


def notification_view(request):
    return render(request, 'home/notification.html')

def results_view(request):
    email = request.session.get('user_email')
    if not email:
        return redirect('login')

    student = StudentsAccount.objects.get(email=email)
    # Lấy toàn bộ dữ liệu RecommendCourse
    my_courses = RecommendCourse.objects.filter(status="passed").count()

    # Truyền sang template
    return render(request, 'home/results.html', {'recommend_courses': my_courses})

def teachers(request):
    teachers = Teacher.objects.all()
    return render(request, "home/teachers.html", {"teachers": teachers})

def courses_current(request):
    email = request.session.get('user_email')
    if not email:
        return redirect('login')

    student = StudentsAccount.objects.get(email=email)

    # Khóa học đã đăng ký
    my_courses = RecommendCourse.objects.filter(student_id=student)

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
#=========== chatbot====================
def chat(request):
    return render(request, "home/chat.html")
# ==============================
# Load model PhoGPT-4B-Chat GGUF khi server start
# ==============================
llm = Llama(
    model_path=r"C:\Users\dungdam\.cache\huggingface\hub\models--vinai--PhoGPT-4B-Chat-gguf\snapshots\192f8ac548e5012d28d8703111842c49fef39271\PhoGPT-4B-Chat-Q4_K_M.gguf",
    n_gpu_layers=-1,   # -1 = dùng toàn bộ GPU
    n_ctx=8192
)

# ==============================
# Hàm tạo reply từ model
# ==============================
def generate_reply(user_message):
    prompt = f"""Bạn là trợ lý AI thông minh, trả lời tiếng Việt rõ ràng, ngắn gọn và đúng ngữ cảnh.
    Người dùng: {user_message}
    AI:"""
    output = llm(prompt, max_tokens=256, temperature=0.7)
    return output['choices'][0]['text'].strip() if output.get('choices') else "[AI không trả lời được]"

# ==============================
# View API chat
# ==============================
def chat_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            message = data.get("message", "").strip()
            if not message:
                reply = "Xin vui lòng nhập tin nhắn"
            else:
                try:
                    reply = generate_reply(message)
                except Exception as e:
                    print("Lỗi generate_reply:", e)
                    reply = "[AI không trả lời được, lỗi GPU]"
            return JsonResponse({"reply": reply})
        except Exception as e:
            print("Lỗi chat_api:", e)
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid method"}, status=400)

#==============================================#
def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(ListLesson, id=lesson_id)
    return render(request, "home/lessons.html", {"lesson": lesson})

def log_action(request, lesson_id):
    if request.method == "POST":
        action = request.POST.get("action")
        if action in ['play', 'pause', 'back', 'done']:
            try:
                email = request.session.get('user_email')
                student_acc = StudentsAccount.objects.get(email=email)
                lesson = ListLesson.objects.get(id=lesson_id)

                UserAction.objects.create(
                    user=student_acc,
                    video=lesson,
                    action=action
                )
                return JsonResponse({"status": "ok", "action": action})
            except ListLesson.DoesNotExist:
                return JsonResponse({"status": "error", "message": "Lesson not found"}, status=404)
            except StudentsAccount.DoesNotExist:
                return JsonResponse({"status": "error", "message": "User not found"}, status=404)
        else:
            return JsonResponse({"status": "error", "message": "Invalid action"}, status=400)
    return JsonResponse({"status": "error", "message": "POST request required"}, status=400)


