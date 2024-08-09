from django.db import models

class Word(models.Model):
    word = models.CharField(max_length=100)
    meaning = models.CharField(max_length=255)

    def __str__(self):
        return self.word

class Group(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Test(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    words = models.ManyToManyField(Word)
    group = models.ForeignKey(Group, related_name='tests', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title

class Student(models.Model):
    name = models.CharField(max_length=100)
    test_group = models.ForeignKey('Group', on_delete=models.SET_NULL, null=True, blank=True)
    current_test = models.ForeignKey('Test', on_delete=models.SET_NULL, null=True, blank=True)
    start_index = models.IntegerField(default=0)
    last_index = models.IntegerField(default=0)
    last_saved = models.DateTimeField(auto_now=True)
    note = models.TextField(blank=True, null=True)
    shuffle = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], default='no')  # shuffleフィールドを追加

    def __str__(self):
        return f"{self.name}"
