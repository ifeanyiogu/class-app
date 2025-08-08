from class_session.models import ClassSession, Lecture
from classroom.models import ClassMember
from rest_framework import status
from django.conf import settings


def get_image_url(img, request):
    if settings.DEBUG:
        return f"{settings.HOST_URL}{img.file.url}"
    else:
        return ""

def get(request, pk):
    user = request.user
    if not user.is_authenticated:
        return {
            'error': 'you are not logged in',
            'status':status.HTTP_401_UNAUTHORIZED
        }
    try:
       session = ClassSession.objects.select_related("lecture").get(pk=pk)
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
    lecture = session.lecture
    images = lecture.images.all()
    files = lecture.files.all()
    
    
    data = {
        'images': [
            {
                'tag':img.tag,
                'url': get_image_url(img, request)
            }
            for img in images
        ],
        'files': [
            {
                'tag':fil.tag,
                'filename':fil.file.name,
                'id':fil.pk
            }
            for fil in files
        ],
        "status":status.HTTP_200_OK
    }
    print(data)
    return data