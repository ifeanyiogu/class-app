from django.db import models
from django.contrib.auth import get_user_model
from class_session.models import ClassSession
from django.utils import timezone
from assignment.models import Assignment
from django.core.exceptions import ValidationError

User = get_user_model()


# Create your models here.
class Submission(models.Model):
    SCORES = (
        (0, 'FAIL'),
        (2, 'PASS'),
        (4, 'GOOD'),
        (5, 'EXCELLENT'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_submissions")
    session = models.ForeignKey(ClassSession, on_delete=models.CASCADE, related_name="submissions")
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='all_submissions')
    note = models.TextField()
    marked = models.BooleanField(default=False)
    score = models.PositiveIntegerField(choices=SCORES, null=True, blank=True)
    date = models.DateTimeField(default=timezone.now())
    
    
    def __str__(self):
        return f"{self.user.username} : {self.session.lecture.topic}"
        
    def save(self, *args, **kwargs):
        if not self.session == self.assignment.session:
            raise ValidationError('wrong session of assignment')
        if self.pk is not None:
            old_one = Submission.objects.get(pk=self.pk)
            if old_one.marked:
                self.marked = True
                self.score = old_one.score
            if not old_one.marked and self.marked:
                if self.score is None:
                    raise ValidationError("No score provided before marking")
            if not old_one.marked and not self.marked:
                if self.score is not None:
                    self.marked = True
        else:
            self.marked = False
            self.score = None
            if not self.assignment.is_published:
                raise ValidationError('assignment is not published yet')
            if self.assignment.deadline <= timezone.now():
                raise ValidationError('assignment deadline reached')
            if not self.assignment.session.is_published:
                raise ValidationError('session is not published')
            
        super().save(*args, **kwargs)