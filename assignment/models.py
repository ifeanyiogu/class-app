from django.db import models
from class_session.models import ClassSession
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericRelation

# Create your models here.
class Assignment(models.Model):
    session = models.ForeignKey(ClassSession, on_delete=models.CASCADE, related_name="assignments")
    audio = models.FileField(upload_to="audio/assignments", null=True, blank=True)
    note = models.TextField()
    is_published = models.BooleanField(default=False)
    deadline = models.DateTimeField(null=True, blank=True)
    images = GenericRelation('class_session.Image', related_query_name='images')
    
    def save(self, *args, **kwargs):
        if self.pk is not None:
            old_obj = Assignment.objects.get(pk=self.pk)
            if old_obj.is_published:
                if not self.is_published:
                    self.is_published = True
                if old_obj.deadline is None:
                    self.is_published = False
            if not old_obj.is_published:
                if not self.is_published:
                    self.deadline=None
                if self.is_published:
                    if self.deadline is None:
                        raise ValidationError('set the deadline')
        else:
            if self.is_published:
                if not self.session.is_published:
                    raise ValidationError('session is mot published')
                if self.deadline is None:
                    raise ValidationError('set_deadline_error')
        super().save(*args, **kwargs)
                
   
    
    
    def __str__(self):
        return f"Assignment for {self.session.lecture.topic}"
    