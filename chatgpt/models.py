# models.py

from django.db import models

class UserQuestion(models.Model):
    question = models.TextField()
    response = models.TextField(blank=True, null=True)
    conversation_history = models.JSONField(default=list, blank=True)  # 대화 히스토리 추가
