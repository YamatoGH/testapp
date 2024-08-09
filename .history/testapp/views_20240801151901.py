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

def create_test(request):
    WordFormSet = formset_factory(WordForm, extra=1)
    if request.method == 'POST':
        form = TestForm(request.POST)
        word_formset = WordFormSet(request.POST, prefix='words')
        if form.is_valid() and word_formset.is_valid():
            test = form.save()
            for word_form in word_formset:
                word = word_form.cleaned_data.get('word')
                meaning = word_form.cleaned_data.get('meaning')
                if word and meaning:
                    Word.objects.create(test=test, word=word, meaning=meaning)
            return redirect('test_detail', test.id)
    else:
        form = TestForm()
        word_formset = WordFormSet(prefix='words')

    return render(request, 'testapp/create_test.html', {'form': form, 'word_formset': word_formset})

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

def handle_uploaded_file(f):
    if f.name.endswith('.csv'):
        df = pd.read_csv(f)
    elif f.name.endswith('.xlsx'):
        df = pd.read_excel(f)
    else:
        raise ValueError("Unsupported file format")
    return df

def create_test_from_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            df = handle_uploaded_file(request.FILES['file'])
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            group = form.cleaned_data['group']
            test = Test.objects.create(title=title, description=description, group=group)

            for _, row in df.iterrows():
                word, created = Word.objects.get_or_create(word=row['word'], defaults={'meaning': row['meaning']})
                test.words.add(word)

            return redirect('quiz:home')
    else:
        form = UploadFileForm()
    return render(request, 'quiz/create_test_from_file.html', {'form': form})