from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now as _now
from datetime import timedelta
from classroom.models import ClassRoom
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

User = get_user_model()

# Create your models here.
class ClassSession(models.Model):
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name="sessions")
    is_published = models.BooleanField(default=False)
    is_expired = models.BooleanField(default=False)
    duration = models.PositiveBigIntegerField(default=45)
    date = models.DateTimeField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if self.pk is not None:
            old_pub = ClassSession.objects.get(pk=self.pk).is_published
            if old_pub and not self.is_published:
                raise ValidationError('Cannot unpublish this Session')
            old_date = ClassSession.objects.get(pk=self.pk).date
            if not old_pub and self.is_published:
                self.date = _now()
            if not old_pub and not self.is_published:
                self.date = None
            if old_pub:
                self.date = old_date
        else:
            self.date = None
            self.is_expired = False
            self.is_published = False
        if self.date is not None:
            expire_time = self.date + timedelta(minutes=self.duration)
            if _now() >= expire_time:
                self.is_expired = True
            else:
                self.is_expired = False
        else:
            self.is_expired = False
            
        super().save(*args, **kwargs)
            
                
    
    
class Lecture(models.Model):
    session = models.OneToOneField(ClassSession, on_delete=models.CASCADE, related_name='lecture')
    topic = models.CharField(max_length=100)
    note = models.TextField()
    audio = models.FileField(upload_to="voice_notes/", null=True, blank=True)
    images = GenericRelation("Image", related_query_name="lecture_image")
    files = GenericRelation("File", related_query_name="lecture_file")
    
    
class Image(models.Model):
    session = models.ForeignKey(ClassSession, on_delete=models.CASCADE, related_name="images")
    file = models.FileField(upload_to="images/")
    tag = models.CharField(max_length=20)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveBigIntegerField()
    content_object = GenericForeignKey('content_type','object_id')
    
    def __str__(self):
        return f'{self.content_type} --{self.tag}'
    
    
class File(models.Model):
    session = models.ForeignKey(ClassSession, on_delete=models.CASCADE, related_name="files")
    file = models.FileField(upload_to="files/")
    tag = models.CharField(max_length=20)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveBigIntegerField()
    content_object = GenericForeignKey('content_type','object_id')
    
    def __str__(self):
        return f'{self.content_type} --{self.tag}'