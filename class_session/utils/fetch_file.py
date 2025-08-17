
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
    try:
        if settings.DEBUG:
            return f"{settings.HOST_URL}{img.file.url}"
        else:
            return img.file.url
    except Exception as e:
        print(str(e))
        return ''


def get(request, pk, obj, i):
    user = request.user
    
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
        if not session.is_published:
            return {
                'error':'Session is not public cannot...',
                'status':status.HTTP_400_BAD_REQUEST
            }
        try:
            main_obj = Lecture.objects.prefetch_related('files').get(pk=i)
        except Lecture.DoesNotExist:
            return {
                'error': 'Invalid lecture id',
                'status':status.HTTP_404_NOT_FOUND
            }
   
    elif obj == "submission":
        try:
            main_obj = Submission.objects.prefetch_related('files').get(pk=i)
        except Submission.DoesNotExist:
            return {
                'error': 'Invalid Submission id',
                'status':status.HTTP_404_NOT_FOUND
            }    
    else:
        return {
            'error': 'Invalid object id',
            'status':status.HTTP_404_NOT_FOUND
        }
    all_files = main_obj.files.all()
    data = [
        {
            'id':fil.pk,
            'name':fil.file.name,
            'url':get_image_url(fil)
        }
        for fil in all_files
    ]
    return {
        'data':data,
        'status': status.HTTP_200_OK
    }