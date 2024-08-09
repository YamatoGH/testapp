from django import forms
from .models import Test, Word, Group
from .models import Student

class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['title', 'description']

class WordForm(forms.ModelForm):
    class Meta:
        model = Word
        fields = ['word', 'meaning']

WordFormSet = forms.inlineformset_factory(Test, Word, form=WordForm, extra=5)

    def save(self, commit=True):
        instance = super(TestForm, self).save(commit=False)
        if commit:
            instance.save()
            words_data = self.cleaned_data['words']
            words_list = words_data.split(',')
            for word_pair in words_list:
                if word_pair:
                    word, meaning = word_pair.split(':')
                    word_obj, created = Word.objects.get_or_create(word=word.strip(), meaning=meaning.strip())
                    instance.words.add(word_obj)
        return instance

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