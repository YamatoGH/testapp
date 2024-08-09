from django import forms
from .models import Test, Word, Group
from .models import Student

class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['name']

class WordForm(forms.Form):
    word = forms.CharField(max_length=100, label='Word')
    meaning = forms.CharField(max_length=255, label='Meaning')

class UploadFileForm(forms.Form):
    file = forms.FileField()
    test_name = forms.CharField(max_length=100)


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name']

class StudentDetailForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'test_group', 'current_test', 'start_index', 'last_index', 'note', 'shuffle']  # shuffleを追加

    shuffle = forms.ChoiceField(
        choices=[('yes', 'Yes'), ('no', 'No')],
        label='Shuffle words',
        initial='no',
        widget=forms.Select(),
        required=True
    )
