from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from .models import Word, Test, Group, Student
from .forms import UploadFileForm
import pandas as pd

class TestAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    change_list_template = "admin/testapp/test_change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-excel/', self.import_excel, name='import-excel'),
        ]
        return custom_urls + urls

    def import_excel(self, request):
        if request.method == "POST":
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                file = request.FILES['file']
                if file.name.endswith('.csv'):
                    data = pd.read_csv(file)
                elif file.name.endswith('.xlsx'):
                    data = pd.read_excel(file)
                else:
                    self.message_user(request, "Unsupported file format", level='error')
                    return redirect("..")

                for index, row in data.iterrows():
                    word, created = Word.objects.get_or_create(word=row['word'], meaning=row['meaning'])
                    self.message_user(request, f"Successfully imported: {word.word}", level='success')

                return redirect("..")
        else:
            form = UploadFileForm()

        context = {
            'form': form,
            'title': "Import Excel",
        }
        return render(request, "admin/testapp/import_excel.html", context)

admin.site.register(Test, TestAdmin)
admin.site.register(Word)
admin.site.register(Group)
admin.site.register(Student)
