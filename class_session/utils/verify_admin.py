from class_session.models import ClassSession
from rest_framework import status
from classroom.models import ClassMember

def verify(user, classroom):
    if not user.is_authenticated:
        return {
            'error': 'you are not logged in',
            'status':status.HTTP_401_UNAUTHORIZED
        }
    
    try:
        member = ClassMember.objects.get(user=user, classroom=classroom, is_approved=True, role='admin')
    except ClassMember.DoesNotExist:
        if not classroom.creator == user:
            return {
                'error': 'You Are Not An Admin',
                'status':status.HTTP_401_UNAUTHORIZED
            }
    return {}