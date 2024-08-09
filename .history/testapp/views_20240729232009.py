from django.shortcuts import render, get_object_or_404, redirect
from .models import Test, Word, Student
from .forms import TestForm, WordFormSet, StudentDetailForm

def create_test(request):
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            test = form.save()
            return redirect('home')
    else:
        form = TestForm()
    return render(request, 'testapp/create_test.html', {'form': form})

def test_detail(request, pk):
    test = get_object_or_404(Test, pk=pk)
    words = test.words.all()
    return render(request, 'testapp/test_detail.html', {'test': test, 'words': words})

def all_tests(request):
    tests = Test.objects.all()
    return render(request, 'testapp/all_tests.html', {'tests': tests})

def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentDetailForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            if request.POST.get('redirect_to_print') == 'yes':
                return redirect('print_test', pk=student.current_test.pk, start_index=student.start_index, end_index=student.last_index, shuffle='no')
            return redirect('student_detail', pk=student.pk)
    else:
        form = StudentDetailForm(instance=student)
    return render(request, 'testapp/student_detail.html', {'student': student, 'form': form})
