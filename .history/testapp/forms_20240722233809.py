from django import forms
from .models import Student, Test

class StudentDetailForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'test_group', 'current_test', 'start_index', 'last_index', 'notes']

class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['title', 'description', 'group']
