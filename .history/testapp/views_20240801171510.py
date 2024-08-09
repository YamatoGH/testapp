import pandas as pd
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Test, Word, Student, Group
from .forms import TestForm, WordForm, StudentDetailForm, UploadFileForm
import random
from django.forms import formset_factory

def home(request):
    groups = Group.objects.all()
    return render(request, 'testapp/home.html', {'groups': groups})

def create_test_from_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            test_name = form.cleaned_data['test_name']
            file = request.FILES['file']
            if file.name.endswith('.csv'):
                data = pd.read_csv(file)
            elif file.name.endswith('.xlsx'):
                data = pd.read_excel(file)
            else:
                messages.error(request, "Unsupported file format")
                return redirect('create_test_from_file')

            group = form.cleaned_data['group']
            test = Test.objects.create(name=test_name, group=group)

            for _, row in data.iterrows():
                Word.objects.create(test=test, word=row['word'], meaning=row['meaning'])

            messages.success(request, "Test created successfully")
            return redirect('test_detail', pk=test.id)
    else:
        form = UploadFileForm()
    
    return render(request, 'testapp/create_test_from_file.html', {'form': form})

def test_detail(request, pk):
    test = get_object_or_404(Test, pk=pk)
    words = test.words.all()
    return render(request, 'testapp/test_detail.html', {'test': test, 'words': words})

def all_tests(request):
    tests = Test.objects.all()
    return render(request, 'testapp/all_tests.html', {'tests': tests})

def print_test(request, pk, start_index, end_index, shuffle):
    test = get_object_or_404(Test, pk=pk)
    words = list(test.words.all())
    if shuffle == 'yes':
        random.shuffle(words)
    words = words[start_index:end_index]
    return render(request, 'testapp/print_test.html', {'test': test, 'words': words})

def print_test_with_answers(request, pk, start_index, end_index, shuffle):
    test = get_object_or_404(Test, pk=pk)
    words = list(test.words.all())
    if shuffle == 'yes':
        random.shuffle(words)
    words = words[start_index:end_index]
    return render(request, 'testapp/print_test_with_answers.html', {'test': test, 'words': words})

def add_student(request):
    if request.method == 'POST':
        form = StudentDetailForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
        else:
            messages.error(request, "Form is not valid")
    else:
        form = StudentDetailForm()
    return render(request, 'testapp/add_student.html', {'form': form})

def student_list(request):
    students = Student.objects.all()
    return render(request, 'testapp/student_list.html', {'students': students})

def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentDetailForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, '保存に成功しました。')
            if 'print' in request.POST:
                return redirect('print_test', pk=student.current_test.pk, start_index=form.cleaned_data['start_index'], end_index=form.cleaned_data['last_index'], shuffle=form.cleaned_data['shuffle'])
            else:
                return redirect('student_detail', pk=student.pk)
        else:
            messages.error(request, "Form is not valid")
            print(form.errors)  # デバッグ用
    else:
        form = StudentDetailForm(instance=student)

    return render(request, 'testapp/student_detail.html', {'form': form, 'student': student})

def group_tests(request, pk):
    group = get_object_or_404(Group, pk=pk)
    tests = group.tests.all()
    return render(request, 'testapp/group_tests.html', {'group': group, 'tests': tests})
