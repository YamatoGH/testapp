from django import forms
from .models import Test, Word, Group
from .models import Student

class WordForm(forms.Form):
    word = forms.CharField(label='Word', max_length=100)
    meaning = forms.CharField(label='Meaning', max_length=255)

class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['title', 'description', 'group', 'file', 'words']

    def save(self, commit=True):
        instance = super(TestForm, self).save(commit=False)
        if commit:
            instance.save()
        return instance
    
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
