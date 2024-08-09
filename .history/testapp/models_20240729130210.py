from django.db import models

class Test(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    pdf = models.FileField(upload_to='pdfs/', blank=True, null=True)  # ここでpdfsディレクトリに保存

    def __str__(self):
        return self.title

class Word(models.Model):
    word = models.CharField(max_length=200)
    meaning = models.CharField(max_length=200)
    test = models.ForeignKey(Test, related_name='words', on_delete=models.CASCADE)

    def __str__(self):
        return self.word
