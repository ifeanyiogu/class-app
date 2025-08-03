from django.db import models
from django.db.models import Q
from django.contrib.auth import get_user_model
import random

User = get_user_model()

# Create your models here.
class ClassRoom(models.Model):
  name = models.CharField(max_length=255, unique=True)
  room_id = models.CharField(max_length=20, unique=True, null=True, blank=True) 
  creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_classes')
  date = models.DateTimeField(auto_now_add=True)
  
  def save(self, *args, **kwargs):
      if not self.room_id:
          
          uid = str(random.randint(000000000,999999999))
          while True:
            if ClassRoom.objects.filter(room_id=uid).exists():
                uid = str(random.randint(000000000,999999999))
            else:
                break
            
          self.room_id = uid
          super().save(*args, **kwargs)
      else:
          super().save(*args, **kwargs)
  

class ClassMember(models.Model):
  roles = (
    ('member','MEMBER'),
    ('admin', 'ADMIN')
  )
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='classrooms')
  classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name='members')
  is_approved = models.BooleanField(default=False)
  role = models.CharField(max_length=255, choices=roles, default="member")
  date = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return f'{self.user.username} in {self.classroom.name}'
  
  class Meta:
    constraints = [
      models.UniqueConstraint(
        fields=["user", "classroom"],
        name="unique_user_classroom"
      ),
      models.UniqueConstraint(
        fields=["role"],
        condition=Q(role="admin"),
        name="unique_admin"
      )
    ]
    