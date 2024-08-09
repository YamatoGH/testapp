from django.db import models

# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Word(models.Model):
    word = models.CharField(max_length=100)
    meaning = models.CharField(max_length=255)

    def __str__(self):
        return self.word

class Test(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    words = models.ManyToManyField(Word, related_name='tests')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='tests', null=True, blank=True)
    def __str__(self):
        return self.title
