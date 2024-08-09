from django import forms
from .models import Test, Word, Group
from .models import Student

class TestForm(forms.ModelForm):
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True, label='Group')
    name = forms.CharField(label='Test Name', required=True)
    class Meta:
        model = Test
        fields = ['name', 'group']

class WordForm(forms.Form):
    word = forms.CharField(max_length=100, label='Word')
    meaning = forms.CharField(max_length=255, label='Meaning')

class UploadFileForm(forms.Form):
    file = forms.FileField()
    


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
