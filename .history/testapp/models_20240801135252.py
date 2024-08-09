from django.db import models

class Group(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Test(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    group = models.ForeignKey(Group, related_name='tests', on_delete=models.CASCADE, null=True, blank=True)
    file = models.FileField(upload_to='test_files/', null=True, blank=True)

    def __str__(self):
        return self.title

class Word(models.Model):
    test = models.ForeignKey(Test, related_name='words', on_delete=models.CASCADE)
    word = models.CharField(max_length=100)
    meaning = models.CharField(max_length=255)

    def __str__(self):
        return self.word
    
class Student(models.Model):
    name = models.CharField(max_length=100)
    test_group = models.ForeignKey('Group', on_delete=models.SET_NULL, null=True, blank=True)
    current_test = models.ForeignKey('Test', on_delete=models.SET_NULL, null=True, blank=True)
    start_index = models.IntegerField(default=0)
    last_index = models.IntegerField(default=0)
    last_saved = models.DateTimeField(auto_now=True)
    note = models.TextField(blank=True, null=True)
    shuffle = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], default='no')

    def __str__(self):
        return self.name
