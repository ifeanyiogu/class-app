from django.db import models
from django.contrib.auth import get_user_model
from class_session.models import ClassSession

User = get_user_model()
# Create your models here.
class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="attendance")
    session = models.ForeignKey(ClassSession, on_delete=models.CASCADE, related_name="session_attendance")
    date = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user','session'], name='unique_user_attendance')
        ]