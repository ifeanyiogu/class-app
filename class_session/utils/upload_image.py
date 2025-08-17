from PIL import Image as PILImage
from io import BytesIO
from django.core.files.base import ContentFile
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


def handle_uploaded_file(file):
    try:
        img = PILImage.open(file)       # Opens the uploaded file
        img.verify()      # e.g., JPEG, PNG, WEBP
    except Exception:
        return {'error': "Invalid image file", 'status':status.HTTP_400_BAD_REQUEST}
    return {'format':img.format}

def convert_to_webp(uploaded_file, quality=80):
    img = PILImage.open(uploaded_file)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    buffer = BytesIO()
    img.save(buffer, format="WEBP", quality=quality)
    return ContentFile(buffer.getvalue(), name=os.path.splitext(uploaded_file.name)[0] + ".webp")

def post(request, pk, obj, i):
    user = request.user
    payload = request.FILES.get('image')
    
    if not payload:
        return {
            'error': 'no image file provided',
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
    img_format = handle_uploaded_file(payload)
    if img_format.get('error'):
        return img_format
    
   
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
    elif obj == "assignment":
        try:
            main_obj = Assignment.objects.get(pk=i)
        except Assignment.DoesNotExist:
            return {
                'error': 'Invalid assignment id',
                'status':status.HTTP_404_NOT_FOUND
            }
        if main_obj.is_published:
            return {
                'error':'assignment already published ',
                'status':status.HTTP_400_BAD_REQUEST
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
    
    image = Image.objects.create(
                session=session,
                file=convert_to_webp(payload),
                content_type=content_t,
                object_id=main_obj.pk, 
            )
    return {
        'url':get_image_url(image),
        'status': status.HTTP_200_OK
    }