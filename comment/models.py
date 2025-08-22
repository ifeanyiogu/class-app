from django.db import models
from django.contrib.auth import get_user_model
from class_session.models import ClassSession
from django.core.exceptions import ValidationError

User = get_user_model()
# Create your models here.
class Comment(models.Model):
    session = models.ForeignKey(ClassSession, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments')
    note = models.TextField()
    date =models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if self.session.is_expired:
            raise ValidationError('session is over')
        if not self.session.is_published:
            raise ValidationError('session is not published yet')
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f'{self.session.lecture.topic}:- {self.note}'
        

class Reply(models.Model):
    session = models.ForeignKey(ClassSession, on_delete=models.CASCADE, related_name='session_replies')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_replies')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE,related_name='replies')
    note = models.TextField()
    date =models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.session == self.comment.session:
            raise ValidationError('wrong session')
        super().save(*args, **kwargs)