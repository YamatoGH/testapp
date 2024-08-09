from django.db import models

class Test(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

class Word(models.Model):
    word = models.CharField(max_length=200)
    meaning = models.CharField(max_length=200)
    test = models.ForeignKey(Test, related_name='words', on_delete=models.CASCADE)

    def __str__(self):
        return self.word

class Student(models.Model):
    name = models.CharField(max_length=100)
    start_index = models.IntegerField(null=True, blank=True)
    last_index = models.IntegerField(null=True, blank=True)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
