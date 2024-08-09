from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Test, Word, Student, Group
from .forms import StudentDetailForm, TestForm
import random

def home(request):
    groups = Group.objects.all()
    return render(request, 'testapp/home.html', {'groups': groups})

def create_test(request):
    if request.method == 'POST':
        form = TestForm(request.POST, request.FILES)
        if form.is_valid():
            test = form.save(commit=False)
            if 'file' in request.FILES:
                test.file = request.FILES['file']
            test.save()

            words_data = request.POST.get('words')
            print("Words data received:", words_data)  # 追加のデバッグ用
            if words_data:
                words_list = words_data.split(',')
                for word_pair in words_list:
                    if word_pair:
                        try:
                            word, meaning = word_pair.split(':')
                            print(f"Processing word: {word}, meaning: {meaning}")  # 追加のデバッグ用
                            word_obj, created = Word.objects.get_or_create(word=word.strip(), meaning=meaning.strip())
                            test.words.add(word_obj)  # ManyToManyフィールドに追加
                            print(f"Added word: {word}, meaning: {meaning}")  # 追加のデバッグ用
                        except ValueError:
                            messages.error(request, f"Error processing word pair: {word_pair}")
                            print(f"Error processing word pair: {word_pair}")  # 追加のデバッグ用
            else:
                print("No words data found.")  # デバッグ用
            return redirect('test_detail', pk=test.pk)
        else:
            messages.error(request, "Form is not valid")
            print(form.errors)  # デバッグ用
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
