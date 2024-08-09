import csv
import pandas as pd
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import formset_factory
from .forms import TestForm, WordForm, StudentForm
from .models import Word, Test, Group, Student
import random

def create_test(request):
    WordFormSet = formset_factory(WordForm, extra=1)
    if request.method == 'POST':
        form = TestForm(request.POST, request.FILES)
        formset = WordFormSet(request.POST, prefix='words')
        if form.is_valid() and formset.is_valid():
            test = form.save(commit=False)
            test.save()
            for word_form in formset:
                word = word_form.cleaned_data.get('word')
                meaning = word_form.cleaned_data.get('meaning')
                if word and meaning:
                    word_obj, created = Word.objects.get_or_create(word=word, meaning=meaning)
                    test.words.add(word_obj)
            if 'file' in request.FILES:
                file = request.FILES['file']
                if file.name.endswith('.csv'):
                    reader = csv.reader(file.read().decode('utf-8').splitlines())
                    for row in reader:
                        if len(row) == 2:
                            word, meaning = row
                            word_obj, created = Word.objects.get_or_create(word=word.strip(), meaning=meaning.strip())
                            test.words.add(word_obj)
                elif file.name.endswith('.xlsx'):
                    df = pd.read_excel(file)
                    for _, row in df.iterrows():
                        if len(row) >= 2:
                            word, meaning = row[0], row[1]
                            word_obj, created = Word.objects.get_or_create(word=word.strip(), meaning=meaning.strip())
                            test.words.add(word_obj)
            return redirect('home')
    else:
        form = TestForm()
        formset = WordFormSet(prefix='words')
    return render(request, 'testapp/create_test.html', {'form': form, 'formset': formset})

def all_tests(request):
    tests = Test.objects.all()
    return render(request, 'testapp/all_tests.html', {'tests': tests})

def group_tests(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    tests = group.tests.all()  # 'tests' は 'related_name' に基づく
    return render(request, 'testapp/group_tests.html', {'group': group, 'tests': tests})

def home(request):
    groups = Group.objects.all()
    return render(request, 'testapp/home.html', {'groups': groups})

def test_detail(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    words = test.words.all()
    return render(request, 'testapp/test_detail.html', {'test': test, 'words': words})

def print_test(request, test_id, start_index, end_index, shuffle):
    test = get_object_or_404(Test, id=test_id)
    words = list(test.words.all())
    if shuffle == 'yes':
        random.shuffle(words)
    words = words[start_index:end_index]
    return render(request, 'testapp/print_test.html', {'test': test, 'words': words})

def print_test_with_answers(request, test_id, start_index, end_index, shuffle):
    test = get_object_or_404(Test, id=test_id)
    words = list(test.words.all())
    if shuffle == 'yes':
        random.shuffle(words)
    words = words[start_index:end_index]
    return render(request, 'testapp/print_test_with_answers.html', {'test': test, 'words': words})

def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')  # 生徒一覧ページにリダイレクト
    else:
        form = StudentForm()
    return render(request, 'testapp/add_student.html', {'form': form})

def student_list(request):
    students = Student.objects.all()
    return render(request, 'testapp/student_list.html', {'students': students})