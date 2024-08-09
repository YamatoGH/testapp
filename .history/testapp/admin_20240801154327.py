from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from .models import Word, Test, Group, Student
from .forms import UploadFileForm
import pandas as pd


class WordInline(admin.TabularInline):
    model = Word

class TestAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [WordInline]


class StudentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Test, TestAdmin)
admin.site.register(Word)
admin.site.register(Group)
admin.site.register(Student)
