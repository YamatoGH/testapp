from django import forms
from .models import Test, Word, Group
from .models import Student
from django.forms import modelformset_factory

class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['title', 'description', 'group']  # 'group'を追加

class WordForm(forms.ModelForm):
    class Meta:
        model = Word
        fields = ['word', 'meaning']

WordFormSet = modelformset_factory(Word, form=WordForm, extra=1)
# UploadFileForm の追加
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