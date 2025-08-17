from django.db import models
from django.contrib.auth import get_user_model
from class_session.models import ClassSession
from assignment.models import Assignment
User = get_user_model()

# Create your models here.
class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_submissions")
    session = models.ForeignKey(ClassSession, on_delete=models.CASCADE, related_name="submissions")
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='assignments')
    note = models.TextField()
    
    def __str__(self):
        return f"{self.user.username} : {self.session.lecture.topic}"