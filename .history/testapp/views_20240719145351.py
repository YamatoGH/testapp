from django.shortcuts import render, get_object_or_404, redirect
from .models import Test
import random
from django.forms import formset_factory
from .forms import TestForm, WordForm
from .models import Word, Test, Group
import csv
import pandas as pd

def home(request):
    groups = Group.objects.all()
    return render(request, 'testapp/home.html', {'groups': groups})

def test_detail(request, test_id):
    test = get_object_or_404(Test, pk=test_id)
    words = test.words.all()
    print(f'Test: {test.title}, Words: {list(words)}')  # デバッグログ
    return render(request, 'testapp/test_detail.html', {'test': test, 'words': words})

def print_test(request, test_id, start_index, end_index, shuffle):
    test = get_object_or_404(Test, pk=test_id)
    words = list(test.words.all())[start_index:end_index]
    if shuffle == 'yes':
        random.shuffle(words)  # 単語リストをシャッフル
    return render(request, 'testapp/print_test.html', {'test': test, 'words': words})

def print_test_with_answers(request, test_id, start_index, end_index, shuffle):
    test = get_object_or_404(Test, pk=test_id)
    words = list(test.words.all())[start_index:end_index]
    if shuffle == 'yes':
        random.shuffle(words)  # 単語リストをシャッフル
    return render(request, 'testapp/print_test_with_answers.html', {'test': test, 'words': words})


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
                        word, meaning = row
                        word_obj, created = Word.objects.get_or_create(word=word.strip(), meaning=meaning.strip())
                        test.words.add(word_obj)
                elif file.name.endswith('.xlsx'):
                    df = pd.read_excel(file)
                    for _, row in df.iterrows():
                        word, meaning = row[0], row[1]
                        word_obj, created = Word.objects.get_or_create(word=word.strip(), meaning=meaning.strip())
                        test.words.add(word_obj)
            return redirect('home')
    else:
        form = TestForm()
        formset = WordFormSet(prefix='words')
    return render(request, 'testapp/create_test.html', {'form': form, 'formset': formset})

def group_tests(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    tests = group.tests.all()
    return render(request, 'testapp/group_tests.html', {'group': group, 'tests': tests})