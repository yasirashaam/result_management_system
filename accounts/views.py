from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from accounts.models import Student, Teacher
from results.models import Subject, Marks


# ✅ NEW HOME VIEW
def home(request):
    return redirect('login')


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            print("LOGIN SUCCESS:", user.username)

            if user.role == 'admin':
                return redirect('admin_dashboard')
            elif user.role == 'teacher':
                return redirect('teacher_dashboard')
            else:
                return redirect('student_dashboard')

        return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


@login_required
def admin_dashboard(request):
    return render(request, 'dashboard/admin_dashboard.html', {
        'total_students': Student.objects.count(),
        'total_teachers': Teacher.objects.count(),
        'total_subjects': Subject.objects.count(),
    })


@login_required
def teacher_dashboard(request):
    try:
        teacher = Teacher.objects.get(user=request.user)
        subjects = Subject.objects.filter(teacher=teacher)
    except Teacher.DoesNotExist:
        return redirect('login')
        subjects = []

    return render(request, 'dashboard/teacher_dashboard.html', {
        'subjects': subjects,
        'total_students': Student.objects.count(),
    })


@login_required
def student_dashboard(request):
    try:
        student = Student.objects.get(user=request.user)
        results = Marks.objects.filter(student=student)

        total = sum([r.marks for r in results])
        count = results.count()
        gpa = round(total / count, 2) if count > 0 else 0

    except Student.DoesNotExist:
        results = []
        gpa = 0

    return render(request, 'dashboard/student_dashboard.html', {
        'results': results,
        'gpa': gpa
    })