from django.db import models

# Create your models here.

class UserQuestion(models.Model):
    question = models.TextField()
    response = models.TextField(blank=True, null=True)
