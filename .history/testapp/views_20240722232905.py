from django.shortcuts import render, get_object_or_404, redirect
from .models import Test, Word, Student, Group
from .forms import WordFormSet, StudentDetailForm

def home(request):
    groups = Group.objects.all()
    return render(request, 'testapp/home.html', {'groups': groups})

def create_test(request):
    if request.method == 'POST':
        form = TestForm(request.POST)
        formset = WordFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            test = form.save()
            for wf in formset:
                word, created = Word.objects.get_or_create(word=wf.cleaned_data['word'], meaning=wf.cleaned_data['meaning'])
                test.words.add(word)
            return redirect('home')
    else:
        form = TestForm()
        formset = WordFormSet(queryset=Word.objects.none())
    return render(request, 'testapp/create_test.html', {'form': form, 'formset': formset})

def test_detail(request, pk):
    test = get_object_or_404(Test, pk=pk)
    words = test.words.all()
    return render(request, 'testapp/test_detail.html', {'test': test, 'words': words})

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
            return redirect('student_list')
    else:
        form = StudentDetailForm(instance=student)
    return render(request, 'testapp/student_detail.html', {'form': form, 'student': student})

def group_tests(request, pk):
    group = get_object_or_404(Group, pk=pk)
    tests = group.tests.all()
    return render(request, 'testapp/group_tests.html', {'group': group, 'tests': tests})
