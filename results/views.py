from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .models import Marks
from .forms import MarksForm
from accounts.models import Teacher, Student

from reportlab.pdfgen import canvas


@login_required
def add_marks(request):
    teacher = Teacher.objects.get(user=request.user)

    if request.method == 'POST':
        form = MarksForm(request.POST)
        if form.is_valid():
            mark = form.save(commit=False)
            mark.teacher = teacher
            mark.save()
            return redirect('view_marks')
    else:
        form = MarksForm()

    return render(request, 'marks/add_marks.html', {'form': form})


@login_required
def view_marks(request):
    teacher = Teacher.objects.get(user=request.user)
    marks = Marks.objects.filter(teacher=teacher)

    search = request.GET.get('search')

    if search:
        marks = marks.filter(student__roll_number__icontains=search)

    return render(request, 'marks/view_marks.html', {'marks': marks})


@login_required
def edit_marks(request, pk):
    mark = get_object_or_404(Marks, pk=pk)

    if request.method == 'POST':
        form = MarksForm(request.POST, instance=mark)
        if form.is_valid():
            form.save()
            return redirect('view_marks')
    else:
        form = MarksForm(instance=mark)

    return render(request, 'marks/edit_marks.html', {'form': form})


@login_required
def delete_marks(request, pk):
    mark = get_object_or_404(Marks, pk=pk)
    mark.delete()
    return redirect('view_marks')

@login_required
def download_result(request):
    try:
        student = Student.objects.get(user=request.user)
        results = Marks.objects.filter(student=student)
    except Student.DoesNotExist:
        return redirect('login')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="result.pdf"'

    p = canvas.Canvas(response)

    y = 800
    p.drawString(200, y, "Student Result")

    y -= 40

    for r in results:
        text = f"{r.subject.name}: {r.marks} ({r.grade})"
        p.drawString(100, y, text)
        y -= 20

    p.showPage()
    p.save()

    return response