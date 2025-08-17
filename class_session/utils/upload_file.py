
from django.contrib.contenttypes.models import ContentType
from classroom.models import ClassMember
from rest_framework import status
from django.conf import settings
from django.core.files import File
import os
from class_session.models import ClassSession, Lecture, Image
from submission.models import Submission
from assignment.models import Assignment
from datetime import timedelta
from django.utils import timezone

def get_image_url(img):
    if settings.DEBUG:
        print(img.file.url)
        return f"{settings.HOST_URL}{img.file.url}"
    else:
        return img.file.url


def post(request, pk, obj, i):
    user = request.user
    payload = request.FILES.get('file')
    
    if not payload:
        return {
            'error': 'no file provided',
            'status':status.HTTP_400_BAD_REQUEST
        }
    if not user.is_authenticated:
        return {
            'error': 'you are not logged in',
            'status':status.HTTP_401_UNAUTHORIZED
        }
    try:
       session = ClassSession.objects.get(pk=pk)
    except ClassSession.DoesNotExist:
        return {
            'error': 'class session does not exist',
            'status':status.HTTP_404_NOT_FOUND
        }
    try:
        member = ClassMember.objects.get(user=user, classroom=session.classroom, is_approved=True)
    except ClassMember.DoesNotExist:
        return {
            'error': 'You Are Not A Member',
            'status':status.HTTP_401_UNAUTHORIZED
        }
  
    main_obj = None
    if obj == "lecture":
        if session.is_published:
            return {
                'error':'Session is already public cannot...',
                'status':status.HTTP_400_BAD_REQUEST
            }
        try:
            main_obj = Lecture.objects.get(pk=i)
        except Lecture.DoesNotExist:
            return {
                'error': 'Invalid lecture id',
                'status':status.HTTP_404_NOT_FOUND
            }
   
    elif obj == "submission":
        try:
            main_obj = Submission.objects.get(pk=i)
        except Submission.DoesNotExist:
            return {
                'error': 'Invalid Submission id',
                'status':status.HTTP_404_NOT_FOUND
            }
        if main_obj.assignment.deadline is not None and main_obj.assignment.deadline <= timezone.now():
            return {
                'error':'assignment deadline is reached',
                'status':status.HTTP_400_BAD_REQUEST
            }
            
    else:
        return {
            'error': 'Invalid object id',
            'status':status.HTTP_404_NOT_FOUND
        }
    content_t = ContentType.objects.get_for_model(main_obj)  
    
    file = File.objects.create(
                session=session,
                file=payload,
                content_type=content_t,
                object_id=main_obj.pk, 
            )
    return {
        'url':get_image_url(file),
        'status': status.HTTP_200_OK
    }