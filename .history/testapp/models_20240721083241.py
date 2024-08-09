from django.db import models

class Group(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Test(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    words = models.ManyToManyField('Word', blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='tests', null=True, blank=True)

    def __str__(self):
        return self.title

class Word(models.Model):
    word = models.CharField(max_length=100)
    meaning = models.CharField(max_length=255)

    def __str__(self):
        return self.word

class Student(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} "