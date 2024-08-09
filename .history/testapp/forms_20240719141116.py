# testapp/forms.py
from django import forms
from .models import Test, Word, Group

class UploadFileForm(forms.Form):
    file = forms.FileField()



class WordForm(forms.Form):
    word = forms.CharField(label='Word', max_length=100)
    meaning = forms.CharField(label='Meaning', max_length=255)

class TestForm(forms.ModelForm):
    file = forms.FileField(required=False, help_text='Upload an Excel or CSV file')
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=False)

    class Meta:
        model = Test
        fields = ['title', 'description', 'group']

    words = forms.CharField(widget=forms.HiddenInput(), required=False)

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