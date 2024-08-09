from django import forms
from .models import Test, Word, Group
from .models import Student

class WordForm(forms.Form):
    word = forms.CharField(label='Word', max_length=100)
    meaning = forms.CharField(label='Meaning', max_length=255)

class TestForm(forms.ModelForm):
    file = forms.FileField(required=False, help_text='Upload a CSV file with words and meanings')
    words = forms.CharField(widget=forms.HiddenInput(), required=False)
    word = forms.CharField(label='Word', max_length=100, required=False)
    meaning = forms.CharField(label='Meaning', max_length=255, required=False)

    class Meta:
        model = Test
        fields = ['title', 'description', 'group', 'file', 'words', 'word', 'meaning']

    def save(self, commit=True):
        instance = super(TestForm, self).save(commit=False)
        if commit:
            instance.save()
        return instance
    
class UploadFileForm(forms.Form):
    file = forms.FileField()
    title = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=False)

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
