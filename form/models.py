from django.db import models


class Form(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Result(models.Model):
    answer = models.BooleanField(default=False)
    coment = models.CharField(max_length=100, null=True, blank=True)
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='from_instance')
    
    def __str__(self) -> str:
        return str(self.form)